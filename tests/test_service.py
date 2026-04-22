from solar_scale.units import parse_length
from solar_scale.service import build_anchor, scale_from_anchor


def test_same_internal_scale_for_equivalent_inputs():
    imperial = parse_length(142, "ft")
    metric = parse_length(43.2816, "m")

    a1 = build_anchor("Neptune", imperial.meters, imperial.original_unit)
    a2 = build_anchor("Neptune", metric.meters, metric.original_unit)

    r1 = scale_from_anchor(a1)
    r2 = scale_from_anchor(a2)

    earth1 = next(item for item in r1 if item.name == "Earth")
    earth2 = next(item for item in r2 if item.name == "Earth")

    assert round(earth1.scaled_distance_m, 9) == round(earth2.scaled_distance_m, 9)

def test_sun_is_included_in_output():
    anchor = build_anchor("Neptune", 43.2816, "ft")
    results = scale_from_anchor(anchor)

    sun = next(item for item in results if item.name == "Sun")
    assert sun.scaled_distance_m == 0
    assert sun.scaled_diameter_mm > 0