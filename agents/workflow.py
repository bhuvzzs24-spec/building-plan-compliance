
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class ComplianceState(TypedDict):
    building_details: dict
    findings: list[str]
    status: str


def check_proposal(state: ComplianceState) -> ComplianceState:
    """Initial placeholder for the building compliance check."""
    details = state["building_details"]

    findings = []

    if not details:
        findings.append("No building details were provided.")

    return {
        **state,
        "findings": findings,
        "status": "needs_review" if findings else "pending_rules_check",
    }


builder = StateGraph(ComplianceState)
builder.add_node("check_proposal", check_proposal)

builder.add_edge(START, "check_proposal")
builder.add_edge("check_proposal", END)

compliance_workflow = builder.compile()


if __name__ == "__main__":
    result = compliance_workflow.invoke(
        {
            "building_details": {"building_use": "residential"},
            "findings": [],
            "status": "pending",
        }
    )

    print(result)

