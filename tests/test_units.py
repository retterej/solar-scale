from solar_scale.units import meters_to_unit, parse_length


def test_parse_feet_to_meters():
    parsed = parse_length(142, "ft")
    assert round(parsed.meters, 4) == 43.2816


def test_round_trip_feet():
    meters = parse_length(142, "feet").meters
    feet = meters_to_unit(meters, "ft")
    assert round(feet, 6) == 142.0


def test_metric_and_imperial_match():
    a = parse_length(142, "ft").meters
    b = parse_length(43.2816, "m").meters
    assert abs(a - b) < 1e-9