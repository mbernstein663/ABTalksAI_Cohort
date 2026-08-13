import sqlite3
from pathlib import Path
import sys
from typing import Any
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Coverage Chatbot")

db_path = Path(__file__).resolve().parent / "data" / "coverage.db"


@mcp.tool(
    name="check_coverage",
    description="Check whether a procedure (e.g. surgery, X-ray) is covered under a specific insurance plan (e.g. Gold PPO), identified by a plan ID e.g. P101"
)
def check_coverage(plan_id: str, procedure: str) -> dict[str, Any]:

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT CASE
                WHEN COUNT(*) > 0 THEN 1
                ELSE 0
            END
            FROM claims
            WHERE plan_id = ?
              AND procedure = ?
            """,
            (plan_id, procedure)
        )

        covered = bool(cursor.fetchone()[0])

    return {
        "plan_id": plan_id,
        "procedure": procedure,
        "covered": covered
    }


@mcp.tool(
    name="get_claim_status",
    description="Check status of a current claim specified by claim ID e.g. C1003"
)
def get_claim_status(claim_id: str) -> dict[str, Any]:

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT status
            FROM claims
            WHERE claim_id = ?
            """,
            (claim_id,)
        )

        row = cursor.fetchone()

    if row is None:
        return {
            "claim_id": claim_id,
            "status": None
        }

    return {
        "claim_id": claim_id,
        "status": row[0]
    }


if __name__ == "__main__":
    print("STARTING MCP SERVER", file=sys.stderr)
    mcp.run()