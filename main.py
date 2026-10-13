
from fastapi import FastAPI

app = FastAPI(
    title="Building Plan Compliance Pre-Check",
    version="0.1.0",
)


@app.get("/")
def home():
    return {
        "message": "Building Plan Compliance API is running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
