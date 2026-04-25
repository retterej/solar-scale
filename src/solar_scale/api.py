from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .formatting import format_body
from .models import Body
from .service import build_anchor, build_anchor_from_size, load_bodies, scale_from_anchor
from .units import parse_length

app = FastAPI(
    title="Solar Scale API",
    description=(
        "Scale the solar system to any size. "
        "Provide an anchor object with either an orbital distance or a physical diameter, "
        "and get back scaled positions and sizes for every body in the system."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/health", summary="Health check")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/bodies", summary="List all solar system bodies", response_model=list[Body])
def bodies() -> list[Body]:
    return load_bodies()


@app.get("/scale", summary="Scale the solar system from an anchor object")
def scale(
    object_name: str,
    unit: str,
    orbit: float | None = None,
    size: float | None = None,
) -> list[dict[str, Any]]:
    if size is not None:
        parsed = parse_length(size, unit)
        try:
            anchor = build_anchor_from_size(object_name, parsed.meters, parsed.original_unit)
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))
    elif orbit is not None:
        parsed = parse_length(orbit, unit)
        try:
            anchor = build_anchor(object_name, parsed.meters, parsed.original_unit)
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))
    else:
        raise HTTPException(status_code=422, detail="Provide either 'orbit' or 'size'")

    results = scale_from_anchor(anchor)
    return [format_body(item, anchor.preferences).model_dump() for item in results]
