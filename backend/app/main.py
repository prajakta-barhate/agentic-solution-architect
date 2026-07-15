from fastapi import FastAPI

app = FastAPI(title="Agentic Solution Architect API")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
