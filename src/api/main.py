"""PlantMind FastAPI application.

Run:
    uvicorn src.api.main:app --reload
    # or
    python -m src.api.main

Docs: http://localhost:8000/docs
"""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.analyze import router as analyze_router
from src.api.routes.audit_log import router as audit_router
from src.api.routes.decisions import router as decisions_router
from src.api.routes.health_check import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Warm up: ensure audit DB tables exist
    from src.governance.audit import _connect
    _connect().close()
    yield


app = FastAPI(
    title="PlantMind API",
    description="Physics-informed engineering intelligence — GötzeEngine decision loop.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PREFIX = "/api/v1"
app.include_router(health_router, prefix=PREFIX, tags=["health"])
app.include_router(analyze_router, prefix=PREFIX, tags=["pipeline"])
app.include_router(decisions_router, prefix=PREFIX, tags=["decisions"])
app.include_router(audit_router, prefix=PREFIX, tags=["audit"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
