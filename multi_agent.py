from typing import TypedDict, Literal
import ollama
from langgraph.graph import StateGraph, START, END
from langchain_agent import retrieve, load_history, summarize_history
import sys
from pathlib import Path
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
import traceback

from langchain_agent import retrieve, mcp_client

root = Path(r"C:\Users\micro\Documents\ABTalksAI-Cohort")

async def retrieve_with_retry(question, retries=1, timeout=30):
    for attempt in range(retries + 1):
        try:
            return await asyncio.wait_for(
                retrieve(question),
                timeout=timeout
            )

        except asyncio.TimeoutError:
            print(
                f"Retrieval timeout "
                f"(attempt {attempt + 1}/{retries + 1})"
            )

        except Exception as e:
            print(
                f"Retrieval error "
                f"(attempt {attempt + 1}/{retries + 1}): {e}"
            )
            traceback.print_exception(type(e), e, e.__traceback__)

        if attempt < retries:
            await asyncio.sleep(1)

    # fallback path
    return (
        "I'm having trouble accessing that right now. "
        "Please contact member support.",
        "fallback",
        [],
        None
    )

mcp_client = MultiServerMCPClient(
    {
        "insurance": {
            "transport": "stdio",
            "command": sys.executable,
            "args": [str(root / "mcp_server.py")],
        }
    }
)

async def load_tools():
    tools = await mcp_client.get_tools()
    for tool in tools:
        print(tool.name)

    tool_map = {
        tool.name: tool
        for tool in tools
    }

    coverage_tools = [
        tool_map["check_coverage"],
        tool_map["get_plan_details"],
        tool_map["estimate_out_of_pocket_cost"],
    ]

    claims_tools = [
        tool_map["get_claim_status"],
    ]
    return coverage_tools, claims_tools

class AgentState(TypedDict):
    session_id: int
    question: str
    route: str
    instructions: str
    context: str
    structure: str
    chunk_ids: list
    tool_result: dict | None
    answer: str

def get_question_with_history(state: AgentState):

    question = state["question"]
    session_id = state["session_id"]

    summarize_history(
        session_id,
        token_limit=2000
    )

    history = load_history(
        session_id,
        limit=10
    )

    return f"""
Conversation history:
{history}

Current question:
{question}
"""

def router(state: AgentState):
    question = get_question_with_history(state)

    prompt = f"""
Classify the user's question into exactly one category to invoke the correct specialist:

coverage
claims

Coverage includes:
- plan benefits
- premiums
- deductibles
- copays
- coinsurance
- covered services
- out-of-pocket costs

Claims includes:
- claim status
- claim amounts
- denied claims
- processed claims
- questions about a specific claim

Clearly classify the question using exactly one routing label:
coverage
claims

Question and conversation context:
{question}
"""

    response = ollama.chat(
        model="qwen3:8b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    router_output = response["message"]["content"].strip().lower()

    if "coverage" in router_output and "claims" not in router_output:
        route = "coverage"

    elif "claims" in router_output and "coverage" not in router_output:
        route = "claims"

    else:
        raise ValueError(f"Ambiguous router output: {router_output}")
    return {"route": route}




# -------------------------
# AGENT 2: COVERAGE SPECIALIST
# -------------------------

async def coverage_specialist(state: AgentState):

    question = get_question_with_history(state)


    instructions = """
You are the Coverage Specialist.

Answer questions about:
- plan coverage
- benefits
- premiums
- deductibles
- copays
- coinsurance
- covered services
- out-of-pocket costs

Use retrieved information and tools.
Do not invent information.
"""

    context, structure, chunk_ids, tool_result = (
        await retrieve_with_retry(question)
    )


    return {
        "instructions": instructions,
        "context": context,
        "structure": structure,
        "chunk_ids": chunk_ids,
        "tool_result": tool_result
    }






# -------------------------
# AGENT 3: CLAIMS SPECIALIST
# -------------------------

async def claims_specialist(state: AgentState):

    question = get_question_with_history(state)


    instructions = """
You are the Claims Specialist.

Answer questions about:
- claim status
- claim amounts
- denied claims
- processed claims
- claim payments
- claim-specific issues

Use retrieved information and tools.
Do not invent information.
"""

    context, structure, chunk_ids, tool_result = (
        await retrieve_with_retry(question)
    )

    return {
        "instructions": instructions,
        "context": context,
        "structure": structure,
        "chunk_ids": chunk_ids,
        "tool_result": tool_result
    }

def choose_specialist(state: AgentState) -> Literal["coverage_specialist", "claims_specialist"]:

    if state["route"] == "coverage":
        return "coverage_specialist"

    return "claims_specialist"


# -------------------------
# BUILD GRAPH
# -------------------------


builder = StateGraph(AgentState)

builder.add_node("router", router)
builder.add_node("coverage_specialist", coverage_specialist)
builder.add_node("claims_specialist", claims_specialist)

builder.add_edge(START, "router")

builder.add_conditional_edges(
    "router",
    choose_specialist,
    {
        "coverage_specialist": "coverage_specialist",
        "claims_specialist": "claims_specialist",
    }
)

builder.add_edge("coverage_specialist", END)
builder.add_edge("claims_specialist", END)


# This is what FastAPI will import
graph = builder.compile()


import asyncio

async def main():
    result = await graph.ainvoke({
        "session_id": 1,
        "question": "What is the status of claim C1003?"
    })

    print(result)

if __name__ == "__main__":
    asyncio.run(main())