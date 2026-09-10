import pytest


@pytest.mark.parametrize("weight_input, expected", [
    ("105 lb", 48),
    ("22 kg", 22),
    ("105.3 lb", 48),
    ("22 KG", 22),
    ("22 Pounds", 10),
    # ("1000 g", 1),
    # ("", 0),
    ("-22 lb", -10),
    # ("22",
    ("22 lbs", 10),
    ])
def test_parse_weight_input(weight_input, expected):
    from weight_entry import parse_weight_input
    answer = parse_weight_input(weight_input)
    assert answer == expected
