import pytest


@pytest.mark.parametrize("input_value, error_type", [
    (-4, ValueError),
    ("4", TypeError)
])
def test_calc_square_root_TypeError(input_value, error_type):
    from my_exceptions import calc_square_root
    with pytest.raises(error_type):
        answer = calc_square_root(input_value)
