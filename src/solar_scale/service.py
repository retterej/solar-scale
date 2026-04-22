from __future__ import annotations

import json
from pathlib import Path

from .models import Body, RequestPreferences, ScaleAnchor, ScaledBody
from .units import au_to_m, km_to_mm


def load_bodies() -> list[Body]:
    data_path = Path(__file__).resolve().parents[2] / "data" / "bodies.json"
    raw = json.loads(data_path.read_text())
    return [Body.model_validate(item) for item in raw]


def infer_preferences_from_unit(unit: str) -> RequestPreferences:
    metric_units = {"mm", "cm", "m", "km"}
    normalized = unit.strip().lower()

    if normalized in metric_units:
        return RequestPreferences(
            distance_unit="m",
            size_unit="mm",
            unit_system="metric",
        )

    return RequestPreferences(
        distance_unit="ft",
        size_unit="in",
        unit_system="imperial",
    )


def build_anchor_from_size(object_name: str, target_size_m: float, original_unit: str) -> ScaleAnchor:
    bodies = load_bodies()
    anchor_body = next((b for b in bodies if b.name.lower() == object_name.lower()), None)
    if anchor_body is None:
        raise ValueError(f"Unknown body: {object_name}")

    real_diameter_m = km_to_mm(anchor_body.diameter_km) / 1000
    scale_factor = target_size_m / real_diameter_m
    target_distance_m = au_to_m(anchor_body.semi_major_axis_au) * scale_factor

    preferences = infer_preferences_from_unit(original_unit)
    return ScaleAnchor(
        object_name=object_name,
        target_distance_m=target_distance_m,
        preferences=preferences,
    )


def build_anchor(object_name: str, target_distance_m: float, original_unit: str) -> ScaleAnchor:
    preferences = infer_preferences_from_unit(original_unit)
    return ScaleAnchor(
        object_name=object_name,
        target_distance_m=target_distance_m,
        preferences=preferences,
    )


def scale_from_anchor(anchor: ScaleAnchor) -> list[ScaledBody]:
    bodies = load_bodies()

    anchor_body = next((b for b in bodies if b.name.lower() == anchor.object_name.lower()), None)
    if anchor_body is None:
        raise ValueError(f"Unknown body: {anchor.object_name}")

    anchor_orbit_m = au_to_m(anchor_body.semi_major_axis_au)
    if anchor_orbit_m == 0:
        raise ValueError("Anchor body must have a non-zero orbital distance.")

    meters_per_real_meter = anchor.target_distance_m / anchor_orbit_m

    results: list[ScaledBody] = []

    for body in bodies:
        real_orbit_m = au_to_m(body.semi_major_axis_au)
        real_diameter_mm = km_to_mm(body.diameter_km)

        scaled_distance_m = real_orbit_m * meters_per_real_meter
        scaled_diameter_mm = real_diameter_mm * meters_per_real_meter

        results.append(
            ScaledBody(
                name=body.name,
                kind=body.kind,
                orbit_au=body.semi_major_axis_au,
                diameter_km=body.diameter_km,
                scaled_distance_m=scaled_distance_m,
                scaled_diameter_mm=scaled_diameter_mm,
            )
        )

    return results