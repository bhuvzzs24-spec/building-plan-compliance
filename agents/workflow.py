
from typing import TypedDict, Any

from langgraph.graph import StateGraph, END


class ComplianceState(TypedDict):
    building_details: dict[str, Any]
    findings: list[str]
    status: str


def validate_building_details(state: ComplianceState) -> ComplianceState:
    """Validate the basic building proposal inputs."""

    details = state["building_details"]
    findings = list(state.get("findings", []))

    required_fields = [
        "building_use",
        "plot_area",
        "road_width",
        "proposed_height",
        "zone",
    ]

    for field in required_fields:
        if field not in details:
            findings.append(f"Missing required field: {field}")

    if "plot_area" in details and details["plot_area"] <= 0:
        findings.append("Plot area must be greater than zero.")

    if "road_width" in details and details["road_width"] <= 0:
        findings.append("Road width must be greater than zero.")

    if "proposed_height" in details and details["proposed_height"] <= 0:
        findings.append("Proposed height must be greater than zero.")

    if findings:
        status = "needs_review"
    else:
        status = "pending_rules_check"

    return {
        **state,
        "findings": findings,
        "status": status,
    }


def build_compliance_workflow():
    graph = StateGraph(ComplianceState)

    graph.add_node("validate_building_details", validate_building_details)

    graph.set_entry_point("validate_building_details")
    graph.add_edge("validate_building_details", END)

    return graph.compile()


compliance_workflow = build_compliance_workflow()
