from typing import TypedDict


class Planet(TypedDict):
    name: str
    au: float
    diameter_km: float


class ScaledPlanet(TypedDict):
    name: str
    au: float
    distance_ft: float
    distance_fmt: str
    diameter_in: float


PLANETS: list[Planet] = [
    {"name": "Mercury", "au": 0.387, "diameter_km": 4879},
    {"name": "Venus",   "au": 0.723, "diameter_km": 12104},
    {"name": "Earth",   "au": 1.000, "diameter_km": 12742},
    {"name": "Mars",    "au": 1.524, "diameter_km": 6779},
    {"name": "Jupiter", "au": 5.203, "diameter_km": 139820},
    {"name": "Saturn",  "au": 9.537, "diameter_km": 116460},
    {"name": "Uranus",  "au": 19.191, "diameter_km": 50724},
    {"name": "Neptune", "au": 30.070, "diameter_km": 49244},
]

AU_KM = 149_597_870.7