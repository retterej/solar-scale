from __future__ import annotations

from dataclasses import dataclass


AU_TO_M = 149_597_870_700.0
KM_TO_M = 1_000.0
MM_TO_M = 0.001
CM_TO_M = 0.01
IN_TO_M = 0.0254
FT_TO_M = 0.3048
YD_TO_M = 0.9144
MI_TO_M = 1_609.344

M_TO_MM = 1000.0
M_TO_CM = 100.0
M_TO_KM = 0.001
M_TO_IN = 39.37007874015748
M_TO_FT = 3.280839895013123
M_TO_YD = 1.0936132983377078
M_TO_MI = 0.0006213711922373339


@dataclass(frozen=True)
class ParsedLength:
    meters: float
    original_unit: str


_TO_METERS: dict[str, float] = {
    "mm": MM_TO_M,
    "cm": CM_TO_M,
    "m": 1.0,
    "km": KM_TO_M,
    "in": IN_TO_M,
    "inch": IN_TO_M,
    "inches": IN_TO_M,
    "ft": FT_TO_M,
    "foot": FT_TO_M,
    "feet": FT_TO_M,
    "yd": YD_TO_M,
    "yard": YD_TO_M,
    "yards": YD_TO_M,
    "mi": MI_TO_M,
    "mile": MI_TO_M,
    "miles": MI_TO_M,
}

_FROM_METERS: dict[str, float] = {
    "mm": M_TO_MM,
    "cm": M_TO_CM,
    "m": 1.0,
    "km": M_TO_KM,
    "in": M_TO_IN,
    "ft": M_TO_FT,
    "yd": M_TO_YD,
    "mi": M_TO_MI,
}


def normalize_unit(unit: str) -> str:
    value = unit.strip().lower()
    aliases = {
        "inch": "in",
        "inches": "in",
        "foot": "ft",
        "feet": "ft",
        "yard": "yd",
        "yards": "yd",
        "mile": "mi",
        "miles": "mi",
    }
    return aliases.get(value, value)


def parse_length(value: float, unit: str) -> ParsedLength:
    normalized = normalize_unit(unit)
    if normalized not in _TO_METERS:
        raise ValueError(f"Unsupported unit: {unit}")
    return ParsedLength(meters=value * _TO_METERS[normalized], original_unit=normalized)


def meters_to_unit(meters: float, unit: str) -> float:
    normalized = normalize_unit(unit)
    if normalized not in _FROM_METERS:
        raise ValueError(f"Unsupported unit: {unit}")
    return meters * _FROM_METERS[normalized]


def mm_to_unit(mm: float, unit: str) -> float:
    meters = mm * MM_TO_M
    return meters_to_unit(meters, unit)


def au_to_m(au: float) -> float:
    return au * AU_TO_M


def km_to_mm(km: float) -> float:
    return km * 1_000_000.0