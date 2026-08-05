from typing import Any

import streamlit as st
from pydantic import BaseModel


class ClaimStatusCard(BaseModel):
    claim_id: str
    status: str
    amount: int
    date: str


class CoverageSummaryCard(BaseModel):
    plan_name: str
    deductible: int
    copay: int
    covered: bool


def render_policy_sources(chunk_ids: list[str] | None):
    if not chunk_ids:
        return

    with st.expander("Policy sources"):
        for number, chunk_id in enumerate(chunk_ids, start=1):
            st.markdown(f"{number}. `{chunk_id}`")


def render_tool_card(tool_result: dict[str, Any] | None):
    if not tool_result:
        return

    with st.container(border=True):
        columns = st.columns(len(tool_result))

        for column, (label, value) in zip(
            columns,
            tool_result.items()
        ):
            column.metric(
                label.replace("_", " ").title(),
                value
            )


def render_response_extras(
    chunk_ids: list[str] | None = None,
    tool_result: dict[str, Any] | None = None
):
    render_policy_sources(chunk_ids)
    render_tool_card(tool_result)