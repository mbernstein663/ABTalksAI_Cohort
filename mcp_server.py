import sqlite3
from pathlib import Path

import sys

from mcp.server import MCPServer
from langchain_agent import (
    check_coverage as check_coverage_logic,
    get_claim_status as check_claim,
    vector_lookup,
)
# Replace this import with wherever your Day 10 function lives



mcp = MCPServer("Coverage Chatbot")

db_path = Path(
    r"C:\Users\micro\Documents\ABTalksAI-Cohort\data\coverage.db"
)


@mcp.tool(name="check_coverage", description="check whether procedure is covered under a specific insurance plan")
def check_coverage(plan_id: str, procedure: str, question: str):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
    cursor.execute(
        "SELECT CASE WHEN COUNT(*) > 0 THEN 'True' ELSE 'False' END AS MatchExists FROM claims WHERE plan_id = ? AND procedure = ?",
        (plan_id, procedure,)
    )
    plan = cursor.fetchone()

    vector_results = vector_lookup(question)
    if plan is None:
        return vector_results
    

    # Your existing coverage function
    return check_coverage_logic(plan_id, procedure)

@mcp.tool(name="get_claim_status", description="check status of a current claim specified by claim ID")
def get_claim_status(claim_id: str, question:str):
    prompt = f"SELECT status FROM claims WHERE claim_id = '{claim_id}'"

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
    cursor.execute(prompt)
    status = cursor.fetchone()

    vector_results = vector_lookup(question)
    if status is None:
        return vector_results

    return check_claim(claim_id)


if __name__ == "__main__":
    print("STARTING MCP SERVER", file=sys.stderr)
    mcp.run()
    print("MCP SERVER STOPPED", file=sys.stderr)