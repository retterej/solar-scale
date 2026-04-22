from __future__ import annotations

from typing import Any

from fastapi import FastAPI

from .formatting import format_body
from .service import build_anchor, scale_from_anchor
from .units import parse_length

app = FastAPI(title="Solar Scale API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/scale")
def scale(object_name: str, value: float, unit: str) -> list[dict[str, Any]]:
    parsed = parse_length(value, unit)
    anchor = build_anchor(object_name, parsed.meters, parsed.original_unit)
    results = scale_from_anchor(anchor)
    return [format_body(item, anchor.preferences).model_dump() for item in results]