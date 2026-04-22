from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


DistanceUnit = Literal["mm", "cm", "m", "km", "in", "ft", "yd", "mi"]
SizeUnit = Literal["mm", "cm", "m", "in", "ft"]


class Body(BaseModel):
    name: str
    kind: str = Field(default="planet")
    semi_major_axis_au: float
    diameter_km: float


class RequestPreferences(BaseModel):
    distance_unit: DistanceUnit
    size_unit: SizeUnit
    unit_system: Literal["metric", "imperial"]


class ScaleAnchor(BaseModel):
    object_name: str
    target_distance_m: float
    preferences: RequestPreferences


class ScaledBody(BaseModel):
    name: str
    kind: str
    orbit_au: float
    diameter_km: float

    # canonical internal scaled values
    scaled_distance_m: float
    scaled_diameter_mm: float


class DisplayBody(BaseModel):
    name: str
    kind: str
    orbit_au: float
    distance_display: str
    diameter_display: str