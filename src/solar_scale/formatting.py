from __future__ import annotations

from .models import DisplayBody, RequestPreferences, ScaledBody
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


def format_ft_in(feet: float) -> str:
    ft = int(feet)
    inches = round((feet - ft) * 12, 2)
    if inches >= 12:
        ft += 1
        inches = 0.0
    if ft == 0 and inches == 0.0:
        return "--"
    if ft == 0:
        return f"{inches} in"
    if inches == 0:
        return f"{ft} ft"
    return f"{ft} ft {inches} in"


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


def format_km_m(km: float) -> str:
    k = int(km)
    m = round((km - k) * 1000)
    if m >= 1000:
        k += 1
        m = 0
    if k == 0:
        return f"{m} m"
    if m == 0:
        return f"{k} km"
    return f"{k} km {m} m"


def format_m_cm(meters: float) -> str:
    m = int(meters)
    cm = round((meters - m) * 100)
    if cm >= 100:
        m += 1
        cm = 0
    if m == 0:
        return f"{cm} cm"
    if cm == 0:
        return f"{m} m"
    return f"{m} m {cm} cm"


def format_cm_mm(cm: float) -> str:
    c = int(cm)
    mm = round((cm - c) * 10, 1)
    if mm >= 10:
        c += 1
        mm = 0.0
    if c == 0:
        return f"{mm} mm"
    if mm == 0:
        return f"{c} cm"
    return f"{c} cm {mm} mm"


def format_value(value: float, unit: str) -> str:
    if unit == "ft":
        return format_ft_in(value)
    if unit == "mi":
        return format_mi_ft(value)
    if unit == "km":
        return format_km_m(value)
    if unit == "m":
        return format_m_cm(value)
    if unit == "cm":
        return format_cm_mm(value)
    formatted = f"{round_for_display(value)} {unit}"
    return "--" if formatted == f"0.0 {unit}" else formatted


def format_body(body: ScaledBody, preferences: RequestPreferences) -> DisplayBody:
    if preferences.unit_system == "metric":
        dist_value, dist_unit = _best_unit_from_m(body.scaled_distance_m, _METRIC_DISTANCE_THRESHOLDS)
        size_value, size_unit = _best_unit_from_mm(body.scaled_diameter_mm, _METRIC_SIZE_THRESHOLDS)
    else:
        dist_value, dist_unit = _best_unit_from_m(body.scaled_distance_m, _IMPERIAL_DISTANCE_THRESHOLDS)
        size_value, size_unit = _best_unit_from_mm(body.scaled_diameter_mm, _IMPERIAL_SIZE_THRESHOLDS)

    return DisplayBody(
        name=body.name,
        kind=body.kind,
        orbit_au=body.orbit_au,
        distance_display=format_value(dist_value, dist_unit),
        diameter_display=format_value(size_value, size_unit),
    )
