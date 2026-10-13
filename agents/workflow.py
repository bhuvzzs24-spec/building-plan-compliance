
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class ComplianceState(TypedDict):
    building_details: dict
    findings: list[str]
    status: str


REQUIRED_FIELDS = [
    "building_use",
    "plot_area",
    "road_width",
    "proposed_height",
    "zone",
]


def check_proposal(state: ComplianceState) -> ComplianceState:
    details = state["building_details"]

    findings = [
        f"Missing required field: {field}"
        for field in REQUIRED_FIELDS
        if field not in details or details[field] is None
        or details[field] == ""
    ]

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
    result = compliance_workflow.invoke({
        "building_details": {
            "building_use": "residential",
            "plot_area": 120,
            "road_width": 6,
            "proposed_height": 12,
            "zone": "residential",
        },
        "findings": [],
        "status": "pending",
    })

    print(result)
