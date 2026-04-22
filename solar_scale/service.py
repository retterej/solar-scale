from .data import PLANETS, AU_KM, ScaledPlanet


def scale_system(neptune_distance_ft: float) -> list[ScaledPlanet]:
    neptune = next(p for p in PLANETS if p["name"] == "Neptune")

    feet_per_au = neptune_distance_ft / neptune["au"]

    km_per_au = AU_KM
    feet_per_km = feet_per_au / km_per_au

    results: list[ScaledPlanet] = []

    for p in PLANETS:
        distance_ft = p["au"] * feet_per_au

        diameter_ft = p["diameter_km"] * feet_per_km
        diameter_in = diameter_ft * 12

        results.append({
        "name": p["name"],
        "au": p["au"],
        "distance_ft": distance_ft,
        "distance_fmt": format_feet_inches(distance_ft),
        "diameter_in": diameter_in,
    })

    return results

def format_feet_inches(feet: float) -> str:
    total_inches = feet * 12

    ft = int(total_inches // 12)
    inch = total_inches % 12

    # round to tenths
    inch = round(inch, 1)

    # handle rollover (e.g. 11.95 → 12.0)
    if inch >= 12:
        ft += 1
        inch = 0.0

    if ft == 0:
        return f"{inch:.1f} in"
    if inch == 0:
        return f"{ft} ft"
    return f"{ft} ft {inch:.1f} in"