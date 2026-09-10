import pytest


@pytest.mark.parametrize("hr_bpm, age, age_units, expected", [
    (60, 30, "years", False),
    (60, 14, "years", False),
    (60, 360, "months", False),
    (130, 30, "years", True),
    ])
def test_is_tachycardic(hr_bpm, age, age_units, expected):
    from ecg import is_tachycardic
    answer = is_tachycardic(hr_bpm, age, age_units)
    assert answer == expected


def test_add():
    from ecg import add
    assert add(0.1, 0.2) == pytest.approx(0.3)


"""
pytest -v --cov --cov-report=html test_ecg.py
"""
