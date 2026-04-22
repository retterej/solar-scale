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
            "diameter_in": diameter_in,
        })

    return results