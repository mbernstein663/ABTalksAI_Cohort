from typing import TypedDict, Literal
import ollama
from langgraph.graph import StateGraph, START, END
from langchain_agent import retrieve

class AgentState(TypedDict):
    question: str
    route: str
    instructions: str
    context: str
    structure: str
    chunk_ids: list
    tool_result: dict | None
    answer: str

def router(state: AgentState):
    question = state["question"]

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

Question:
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

def coverage_specialist(state: AgentState):

    question = state["question"]

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

    context, structure, chunk_ids, tool_result = retrieve(question)


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

def claims_specialist(state: AgentState):

    question = state["question"]

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

    context, structure, chunk_ids, tool_result = retrieve(question)

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


if __name__ == "__main__":
    result = graph.invoke({
        "question": "What is the status of claim C1003?"
    })

    print("ROUTE:", result["route"])
    print("ANSWER:", result["answer"])