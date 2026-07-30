import openai
import sqlite3
import ollama
import pandas as pd 
from sentence_transformers import SentenceTransformer
import chromadb
from pathlib import Path

openai.OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

root=Path(r"C:\Users\micro\Documents\ABTalksAI-Cohort")
jsonroot = root / "knowledge_base_embed.jsonl"
db_path = root / "chroma_db"
dpath = root / "data"


dfp = pd.read_csv(dpath / "plans.csv")
dfc = pd.read_csv(dpath / "claims.csv")

conn = sqlite3.connect(dpath / "coverage.db")
dfp.to_sql("plans", conn, if_exists="replace", index=False)
dfc.to_sql("claims", conn, if_exists="replace", index=False)
conn.commit()

client = chromadb.PersistentClient(path=db_path)
collection = client.get_collection(name="coverage_kb")



# write a function that classifies our question using simple keyword classifiers
def define_function(question):
    question = question.lower()

    structured_keywords = [
        "deductible", "premium", "claim status", "claim amount",
        "claim id", "member id", "plan id", "date filed", "copay"
    ]

    unstructured_keywords = [
        "covered", "coverage", "procedure", "prior authorization",
        "appeal", "in-network", "out-of-network", "excluded", "eligible"
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


# call all the functions:
def retrieve(question):
    structure = define_function(question)

    rows = []
    results = {}

    if structure in ("structured", "both"):
        rows = sql_lookup(question) or []

    if structure in ("unstructured", "both"):
        results = vector_lookup(question) or {}

    model_context = merge_context(rows, results)

    print("RAW SQL ROWS:", rows)
    # print("RAW VECTOR RESULTS:", results)

    return model_context, structure



def generate_answer(question, context):
    print("Local chatbot — type 'quit' to exit")
    system_prompt = f"""Answer using ONLY the context below. If the answer isn't in the context, say you don't know and suggest the member contact support. This is not medical advice.

    Context: {context}

    Question: {question}"""

    # 'stream=True' activates streaming mode
    reply = ollama.chat(model='qwen3:8b', messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": question}], stream=True)

    answer = ""
    for chunk in reply:
        text = chunk["message"]["content"]
        answer += text
        print(text, end="", flush=True)

    print()

    return answer



output = root / "rag_qa_results.md"


def retrieve_and_answer(question):
    context, structure = retrieve(question)
    answer = generate_answer(question, context)

    with output.open("a", encoding="utf-8") as file:
        file.write(f"## {question}\n\n")
        file.write(f"{answer}\n\n---\n\n")

    return answer


while (question := input("\nYou: ").strip()).lower() != "quit":
    retrieve_and_answer(question)