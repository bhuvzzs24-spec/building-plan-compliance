
from uuid import uuid4
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

app = FastAPI(
    title="Building Plan Compliance Pre-Check",
    version="0.1.0",
)

runs = {}


class BuildingProposal(BaseModel):
    building_use: str
    plot_area: float
    road_width: float
    proposed_height: float
    zone: str


def process_run(run_id: str, proposal: dict):
    findings = []

    for field in ["building_use", "plot_area", "road_width", "proposed_height", "zone"]:
        if field not in proposal:
            findings.append(f"Missing required field: {field}")

    for field in ["plot_area", "road_width", "proposed_height"]:
        if field in proposal and proposal[field] <= 0:
            findings.append(f"{field} must be greater than zero.")

    runs[run_id]["findings"] = findings
    runs[run_id]["status"] = "needs_review" if findings else "completed"


@app.get("/")
def home():
    return {"message": "Building Plan Compliance API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/runs", status_code=202)
def start_run(proposal: BuildingProposal, background_tasks: BackgroundTasks):
    run_id = str(uuid4())

    runs[run_id] = {
        "run_id": run_id,
        "status": "pending",
        "findings": [],
    }

    background_tasks.add_task(
        process_run,
        run_id,
        proposal.model_dump(),
    )

    return runs[run_id]

@app.get("/runs/{run_id}")
def get_run(run_id: str):
    if run_id not in runs:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Run not found")

    return runs[run_id]
