from pydantic import BaseModel, Field
from langchain.tools import tool
import openai
import sqlite3
import ollama
import pandas as pd 
from sentence_transformers import SentenceTransformer
import chromadb
from pathlib import Path
import tiktoken

from langchain_ollama import ChatOllama
from langchain_classic.agents import (AgentExecutor, create_tool_calling_agent)
from langchain_core.prompts import ChatPromptTemplate

openai.OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

root=Path(r"C:\Users\micro\Documents\ABTalksAI-Cohort")
jsonroot = root / "knowledge_base_embed.jsonl"
db_path = root / "chroma_db"
dpath = root / "data"

output = root / "tool_call_log.md"

dfp = pd.read_csv(dpath / "plans.csv")
dfc = pd.read_csv(dpath / "claims.csv")

conn = sqlite3.connect(
    dpath / "coverage.db",
    check_same_thread=False
)
dfp.to_sql("plans", conn, if_exists="replace", index=False)
dfc.to_sql("claims", conn, if_exists="replace", index=False)
conn.commit()

client = chromadb.PersistentClient(path=db_path)
collection = client.get_collection(name="coverage_kb")











"""
Defining the tools and Pydantic models to call them:

1. Define JSON schema for function object
2. Define actual function operations
3. Pydantic models

"""



# History loader from SQL

import re

def summarize_history(session_id, token_limit=2000):
    with sqlite3.connect(dpath / "coverage.db") as conn:
        rows = conn.execute(
            """
            SELECT rowid, role, content
            FROM conversations
            WHERE session_id = ?
            ORDER BY timestamp ASC, rowid ASC
            """,
            (session_id,)
        ).fetchall()

    history_text = "\n".join(
        f"{role}: {content}"
        for _, role, content in rows
    )

    before_tokens = count_tokens(history_text)

    print(
        f"HISTORY TOKENS | session={session_id} "
        f"| before={before_tokens}"
    )

    if before_tokens <= token_limit:
        print("SUMMARIZATION | triggered=False")
        return

    oldest_half = rows[:len(rows) // 2]

    text_to_summarize = "\n".join(
        f"{role}: {content}"
        for _, role, content in oldest_half
    )

    reply = ollama.chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Summarize this conversation concisely. "
                    "Preserve important facts and identifiers."
                )
            },
            {
                "role": "user",
                "content": text_to_summarize
            }
        ]
    )

    summary = reply["message"]["content"]
    row_ids = [row[0] for row in oldest_half]
    placeholders = ",".join("?" for _ in row_ids)

    with sqlite3.connect(dpath / "coverage.db") as conn:
        conn.execute(
            f"""
            DELETE FROM conversations
            WHERE rowid IN ({placeholders})
            """,
            row_ids
        )

        conn.execute(
            """
            INSERT INTO conversations (
                session_id,
                role,
                content,
                timestamp
            )
            VALUES (?, 'summary', ?, CURRENT_TIMESTAMP)
            """,
            (session_id, summary)
        )

        after_rows = conn.execute(
            """
            SELECT role, content
            FROM conversations
            WHERE session_id = ?
            """,
            (session_id,)
        ).fetchall()

        conn.commit()

    after_text = "\n".join(
        f"{role}: {content}"
        for role, content in after_rows
    )

    print(
        f"SUMMARIZATION | triggered=True "
        f"| after={count_tokens(after_text)}"
    )


def load_history(session_id, limit=10):
    with sqlite3.connect(dpath / "coverage.db") as conn:
        summary = conn.execute(
            """
            SELECT content
            FROM conversations
            WHERE session_id = ?
              AND role = 'summary'
            ORDER BY timestamp DESC, rowid DESC
            LIMIT 1
            """,
            (session_id,)
        ).fetchone()

        rows = conn.execute(
            """
            SELECT role, content
            FROM conversations
            WHERE session_id = ?
              AND role != 'summary'
            ORDER BY timestamp DESC, rowid DESC
            LIMIT ?
            """,
            (session_id, limit)
        ).fetchall()

    rows.reverse()

    history = []

    if summary:
        history.append({
            "role": "system",
            "content": f"Earlier conversation summary: {summary[0]}"
        })

    history.extend(
        {"role": role, "content": content}
        for role, content in rows
    )

    return history




"""
TOOL CALL FUNCTIONS

1. check_coverage: checks to see if a procedure exists for a medical plan (SQL)
2. get_claim_status: checks the status for a customer claim
3. get_plan_details: checks all detailed information about a plan from plans.csv
4. estimate_out_of_pocket_cost: estimates total pricing from a procedure based on the listed coverage


"""



class CoverageInput(BaseModel):
    plan_id: str = Field(
        description="Plan-identifying ID, for example P101"
    )
    procedure: str = Field(
        description="Medical procedure being checked, for example Surgery"
    )


class ClaimStatusInput(BaseModel):
    claim_id: str = Field(
        description="Claim-identifying ID, for example C1001"
    )


class PlanDetailsInput(BaseModel):
    plan_id: str = Field(
        description="Plan-identifying ID, for example P101"
    )


class CostEstimateInput(BaseModel):
    procedure: str = Field(
        description="Medical procedure being estimated, for example Surgery"
    )
    plan_id: str = Field(
        description="Plan-identifying ID, for example P101"
    )


def check_coverage(plan_id, procedure):
    prompt = f"SELECT CASE WHEN COUNT(*) > 0 THEN 'True' ELSE 'False' END AS MatchExists FROM claims WHERE plan_id = '{plan_id}' AND procedure = '{procedure}'"

    cursor = conn.cursor()
    cursor.execute(prompt)
    # columns = [column[0] for column in cursor.description]
    exists = cursor.fetchone()[0] == "True"

    return {
        "plan_id": plan_id,
        "procedure": procedure,
        "covered": exists
    }

def get_claim_status(claim_id):
    prompt = f"SELECT status FROM claims WHERE claim_id = '{claim_id}'"

    cursor = conn.cursor()
    cursor.execute(prompt)
    # columns = [column[0] for column in cursor.description]
    status = cursor.fetchone()[0]

    return {
        "claim_id": claim_id,
        "status": status
    }

def get_plan_details(plan_id):
    normalized_plan = plan_id.replace(" ", "").lower()

    prompt = """
        SELECT
            plan_id,
            plan_name,
            monthly_premium,
            annual_deductible,
            copay_pct,
            coverage_type,
            network_tier
        FROM plans
        WHERE LOWER(plan_id) = ?
           OR REPLACE(LOWER(plan_name), ' ', '') = ?
    """

    cursor = conn.cursor()
    cursor.execute(
        prompt,
        (plan_id.lower(), normalized_plan)
    )

    info = cursor.fetchone()

    if info is None:
        raise ValueError(
            f"No plan found for identifier: {plan_id}"
        )

    return {
        "plan_id": info[0],
        "plan_name": info[1],
        "monthly_premium": info[2],
        "annual_deductible": info[3],
        "copay_pct": info[4],
        "coverage_type": info[5],
        "network_tier": info[6]
    }

def estimate_out_of_pocket_cost(procedure, plan_id):
    prompt = f"SELECT claims.claim_amount * plans.copay_pct / 100.0 AS estimated_out_of_pocket FROM claims JOIN plans ON claims.plan_id = plans.plan_id WHERE claims.plan_id = '{plan_id}' AND claims.procedure = '{procedure}'"

    cursor = conn.cursor()
    cursor.execute(prompt)
    # columns = [column[0] for column in cursor.description]
    row = cursor.fetchone()
    estimate = row[0] if row else None

    return {
        "procedure": procedure,
        "plan_id": plan_id,
        "estimated_cost": estimate
    }



class CoverageOutput(BaseModel):
    plan_id: str
    procedure: str
    covered: bool


class ClaimStatusOutput(BaseModel):
    claim_id: str
    status: str


class PlanDetailsOutput(BaseModel):
    plan_id: str
    plan_name: str
    monthly_premium: int
    annual_deductible: int
    copay_pct: int
    coverage_type: str
    network_tier: str


class CostEstimateOutput(BaseModel):
    procedure: str
    plan_id: str
    estimated_cost: float | None



@tool("check_coverage", args_schema=CoverageInput)
def check_coverage_tool(plan_id: str, procedure: str) -> dict:
    """Check whether historical approved claim data suggests that a procedure is covered under a plan."""

    result = check_coverage(plan_id, procedure)

    return CoverageOutput.model_validate(result).model_dump()

@tool("get_claim_status", args_schema=ClaimStatusInput)
def get_claim_status_tool(claim_id:str) -> dict:
    """Get the current status of a specific insurance claim using its claim ID."""

    result = get_claim_status(claim_id)
    return ClaimStatusOutput.model_validate(result).model_dump()

@tool("get_plan_details", args_schema=PlanDetailsInput)
def get_plan_details_tool(plan_id: str) -> dict:
    """Get premium, deductible, copay, coverage type, network tier, and other details for a specific insurance plan."""

    result = get_plan_details(plan_id)

    return PlanDetailsOutput.model_validate(result).model_dump()

@tool("estimate_out_of_pocket_cost", args_schema=CostEstimateInput)
def estimate_out_of_pocket_cost_tool(procedure: str,plan_id: str) -> dict:
    """Estimate a member's out-of-pocket cost for a specific procedure under a specific insurance plan."""

    result = estimate_out_of_pocket_cost(procedure, plan_id)

    return CostEstimateOutput.model_validate(result).model_dump()


tools = [
    check_coverage_tool,
    get_claim_status_tool,
    get_plan_details_tool,
    estimate_out_of_pocket_cost_tool,
]

"""
Questions:

1. Is surgery covered by the plan with id P101?
2. Are X-rays covered by the plan with id P102?
3. What is my estimated out of pocket cost for a surgery under plan with id P103?
4. What is the status of claim C1004?
5. What are the details for plan P101?

6. How can I appeal if my claim was denied?
"""



llm = ChatOllama(
    model="qwen3:8b",
    temperature=0
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a health insurance coverage support agent. "
        "Use the available tools when the user asks about coverage, "
        "claim status, plan details, or estimated out-of-pocket cost. "
        "Use tool results rather than guessing."
    ),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_intermediate_steps=True
)

# agent_executor = AgentExecutor(
#     agent=agent,
#     tools=tools,
#     verbose=True
# )



"""
FUNCTION DEFINITIONS

TOOL CALLS:
1. Defines whether question is classified as structured or unstructured to aid in retrieval
2. SQL lookup: NON tool call that prompts off-the-cuff SQL generation for structured outputs

"""




# write a function that classifies our question using simple keyword classifiers
def define_function(question):
    question = question.lower()

    structured_keywords = [
        "deductible", "premium", "status", "claim amount", "procedure", "date",
        "claim id", "member id", "plan id", "date filed", "copay", "plan", "claim", "surgery"
    ]

    unstructured_keywords = [
        "cover", "coverage", "procedure", "prior", "detail", "authorization",
        "appeal", "in-network", "out-of-network", "exclud", "eligible", "how"
    ]

    structured_match = any(word in question for word in structured_keywords)
    unstructured_match = any(word in question for word in unstructured_keywords)

    if structured_match and unstructured_match:
        return "both"
    elif structured_match:
        return "structured"
    else:
        return "unstructured"



def sql_lookup(question):
    user = f"""
    Convert the question into exactly one read-only SQLite SELECT statement for structured RAG retrieval.

    Question: {question}

    Database schema:
    plans:plan_id,plan_name,monthly_premium,annual_deductible,copay_pct,coverage_type,network_tier
    claims:claim_id,member_id,plan_id,procedure,claim_amount,status,date_filed

    Return only the SELECT statement.
    Do not use markdown, explanations, or labels.
    DO NOT include code fences like '```sql ... ```'
    Never use INSERT, UPDATE, DELETE, DROP, ALTER, or CREATE.
    DO NOT try to create statements with information that is not explicitly provided.

    Always include identifying columns used in the question or WHERE clause.
    For example, return claim_id with claim_amount and plan_name with monthly_premium.

    Example question: What is the monthly premium for the Gold PPO plan?
    Example output: SELECT plan_name, monthly_premium FROM plans WHERE plan_name = 'Gold PPO';

    Example question: What is the claim status for C1003, and how do I appeal if it was denied?
    Example output: SELECT claim_id, status FROM claims WHERE claim_id = 'C1003';
    """

    reply = ollama.chat(
        model="qwen2.5-coder:14b",
        messages=[
            {"role": "user", "content": user}
        ]
    )

    text = reply["message"]["content"]
    cursor = conn.cursor()
    print("GENERATED SQL:", repr(text))

    no_fly_list = ["```", "delete", "create", "update", "drop", "insert", "alter"]
    if any(word in text.lower() for word in no_fly_list):
        return []

    cursor.execute(text)
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()

    return [dict(zip(columns, row)) for row in rows]

def vector_lookup(question): 

    emb_query = model.encode(question)
    results = collection.query(
        query_embeddings=[emb_query],
        n_results=5,
    )
    return results


def merge_context(rows, results):
    context_items = []

    for row in rows or []:
        context_items.append(f"Structured database result:\n{row}")

    documents = results.get("documents", [[]])[0] if results else []

    for document in documents:
        context_items.append(f"Retrieved document:\n{document}")

    seen = set()
    unique_items = []

    for item in context_items:
        normalized = " ".join(item.lower().split())

        if normalized not in seen:
            seen.add(normalized)
            unique_items.append(item)

    return "\n\n---\n\n".join(unique_items)


def tool_call(question):
    result = agent_executor.invoke({
        "input": question
    })

    reasoning = result.get("intermediate_steps", [])

    print(reasoning)

    with (root / "agent_traces.md").open("a", encoding="utf-8") as file:
        file.write(f"## {question}\n\n")
        file.write("#### Reasoning:\n\n")
        file.write(f"{reasoning}\n\n---\n\n")

    if reasoning:
        return reasoning[-1][1]

    return None








"""
AFTER defining the tools and other context retrieval methods, we call all the functions in "retrieve"'

- question structure and LLM  tool decision decides which tools will be used to create model context
- model_context and structure are then passed to generate answer, where we use the system prompt from Day 12 and the chatbot performs as usual.


"""




# call all the functions:
def retrieve(question):
    structure = define_function(question)
    print("STRUCTURE:", structure)
    rows = []
    results = {}
    tool_result = None
    chunk_ids = []

    if structure in ("structured", "both"):
        tool_result = tool_call(question)

        if tool_result is not None:
            rows = [tool_result]
        else:
            rows = sql_lookup(question) or []

    if structure in ("unstructured", "both"):
        results = vector_lookup(question) or {}

    model_context = merge_context(rows, results)
    chunk_ids = results.get("ids", [[]])[0] if results else []


    print("CHUNK IDS:", chunk_ids)
    # print("RAW VECTOR RESULTS:", results)

    return model_context, structure, chunk_ids, tool_result



def count_tokens(text):
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def generate_answer(question, context, instructions=""):
    print("Local chatbot — type 'quit' to exit")
    system_prompt = f"""
    Specialized Instructions: {instructions}
    
    Answer polietly and succinctly using ONLY the context below. Before compiling your answer, check the plan type, section, and language to validate that the context supports an actual answer. If the answer isn't in the context, say you don't know and suggest the member contact support. Do not give medical advice.

    **Context:** {context}

    **Question:** {question}"""

    # 'stream=True' activates streaming mode
    reply = ollama.chat(model='qwen3:8b', 
        messages=[{"role": "system", "content": system_prompt}, 
        {"role": "user", "content": question}], stream=True
        )

    answer = ""
    for chunk in reply:
        text = chunk["message"]["content"]
        answer += text
        print(text, end="", flush=True)

    print()

    return answer









def retrieve_and_answer(question):
    context, structure = retrieve(question)
    answer = generate_answer(question, context)
    return answer

if __name__ == "__main__":
    while (question := input("\nYou: ").strip()).lower() != "quit":
        retrieve_and_answer(question)



