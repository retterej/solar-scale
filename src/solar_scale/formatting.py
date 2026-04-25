from __future__ import annotations

from .models import DisplayBody, DisplayMeasurement, RequestPreferences, ScaledBody
from .units import meters_to_unit, mm_to_unit

_METRIC_DISTANCE_THRESHOLDS: list[tuple[float, str]] = [
    (1_000, "km"),
    (1, "m"),
    (0.01, "cm"),
    (0, "mm"),
]

_IMPERIAL_DISTANCE_THRESHOLDS: list[tuple[float, str]] = [
    (0.1, "mi"),
    (1, "ft"),
    (0, "in"),
]

_METRIC_SIZE_THRESHOLDS: list[tuple[float, str]] = [
    (1_000, "m"),
    (10, "cm"),
    (0, "mm"),
]

_IMPERIAL_SIZE_THRESHOLDS: list[tuple[float, str]] = [
    (1, "ft"),
    (0, "in"),
]


def _best_unit_from_m(value_m: float, thresholds: list[tuple[float, str]]) -> tuple[float, str]:
    for threshold, unit in thresholds:
        converted = meters_to_unit(value_m, unit)
        if converted >= threshold:
            return converted, unit
    _, fallback_unit = thresholds[-1]
    return meters_to_unit(value_m, fallback_unit), fallback_unit


def _best_unit_from_mm(value_mm: float, thresholds: list[tuple[float, str]]) -> tuple[float, str]:
    return _best_unit_from_m(value_mm / 1000, thresholds)


def round_for_display(value: float) -> float:
    if value >= 100:
        return round(value, 2)
    if value >= 10:
        return round(value, 3)
    if value >= 1:
        return round(value, 4)
    return round(value, 6)


def _fmt_in(inches: float) -> str:
    return f"{inches:.2f}".rstrip("0").rstrip(".")


def format_ft_in(feet: float) -> str:
    ft = int(feet)
    inches = round((feet - ft) * 12, 2)
    if inches >= 12:
        ft += 1
        inches = 0.0
    if ft == 0 and inches == 0.0:
        return "--"
    if ft == 0:
        return f"{_fmt_in(inches)} in"
    if inches == 0:
        return f"{ft} ft"
    return f"{ft} ft {_fmt_in(inches)} in"


def format_mi_ft(miles: float) -> str:
    mi = int(miles)
    feet = round((miles - mi) * 5280)
    if feet >= 5280:
        mi += 1
        feet = 0
    if mi == 0:
        return f"{feet} ft"
    if feet == 0:
        return f"{mi} mi"
    return f"{mi} mi {feet} ft"


def format_value(value: float, unit: str) -> str:
    if unit == "ft":
        return format_ft_in(value)
    if unit == "mi":
        return format_mi_ft(value)
    if unit == "in":
        v = f"{value:.2f}".rstrip("0").rstrip(".")
        return "--" if v == "0" else f"{v} in"
    v = str(round_for_display(value)).rstrip("0").rstrip(".")
    return "--" if v == "0" else f"{v} {unit}"


def _format_distance(value_m: float) -> DisplayMeasurement:
    imp_val, imp_unit = _best_unit_from_m(value_m, _IMPERIAL_DISTANCE_THRESHOLDS)
    met_val, met_unit = _best_unit_from_m(value_m, _METRIC_DISTANCE_THRESHOLDS)
    return DisplayMeasurement(
        imperial=format_value(imp_val, imp_unit),
        metric=format_value(met_val, met_unit),
    )


def _format_diameter(value_mm: float) -> DisplayMeasurement:
    imp_val, imp_unit = _best_unit_from_mm(value_mm, _IMPERIAL_SIZE_THRESHOLDS)
    met_val, met_unit = _best_unit_from_mm(value_mm, _METRIC_SIZE_THRESHOLDS)
    return DisplayMeasurement(
        imperial=format_value(imp_val, imp_unit),
        metric=format_value(met_val, met_unit),
    )


def format_body(body: ScaledBody, preferences: RequestPreferences) -> DisplayBody:
    return DisplayBody(
        name=body.name,
        kind=body.kind,
        orbit_au=body.orbit_au,
        distance=_format_distance(body.scaled_distance_m),
        diameter=_format_diameter(body.scaled_diameter_mm),
    )
