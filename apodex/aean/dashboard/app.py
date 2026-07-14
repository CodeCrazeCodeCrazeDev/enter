"""FastAPI dashboard for the AEAN organism.

Run with::

    pip install fastapi uvicorn
    uvicorn apodex.aean.dashboard.app:app --reload --port 8000

Then open http://localhost:8000 to drive the compounding flywheel, step it
cycle-by-cycle or auto-run, and watch capital compound, cells spawn/kill/scale,
and the Research engine surface insights in real time.

Endpoints:
    GET  /                serves the single-page dashboard
    GET  /api/state       current organism snapshot (JSON)
    POST /api/step        advance N cycles (body: {"cycles": int})
    POST /api/reset       reset with new capital/seed
    GET  /healthz         liveness probe
"""
from __future__ import annotations

import threading
from pathlib import Path
from typing import Optional

try:
    from fastapi import FastAPI
    from fastapi.responses import FileResponse
    from pydantic import BaseModel
except ImportError as exc:  # pragma: no cover - dashboard extras not installed
    raise ImportError(
        "The AEAN dashboard requires FastAPI. Install with: pip install fastapi uvicorn"
    ) from exc

from ..flywheel import Organism

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="AEAN Dashboard", version="1.0.0")

_lock = threading.Lock()
_organism = Organism(initial_capital_cents=100_000_00, seed=7)


class StepRequest(BaseModel):
    cycles: int = 1


class ResetRequest(BaseModel):
    capital: float = 100_000.0
    seed: Optional[int] = 7


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


@app.get("/api/state")
def state() -> dict:
    with _lock:
        return _organism.snapshot()


@app.post("/api/step")
def step(req: StepRequest) -> dict:
    with _lock:
        _organism.run(max(1, min(req.cycles, 100)))
        return _organism.snapshot()


@app.post("/api/reset")
def reset(req: ResetRequest) -> dict:
    global _organism
    with _lock:
        _organism = Organism(initial_capital_cents=int(req.capital * 100), seed=req.seed)
        return _organism.snapshot()
