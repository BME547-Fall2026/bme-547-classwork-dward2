import pytest

@pytest.mark.parametrize("HDL_value, expected", [
    (70, "Normal"),
    (45, "Borderline Low"),
    (20, "Low")])
def test_HDL_analysis(HDL_value, expected):
    # Arrange
    from blood_analysis import HDL_analysis
    # Act
    answer = HDL_analysis(HDL_value)
    # Assert
    assert answer == expected


@pytest.mark.parametrize("LDL_value, expected", [
    (120, "Normal"),
    (135, "Borderline High"),
    (165, "High"),
    (200, "Very High")])
def test_LDL_analysis(LDL_value, expected):
    from blood_analysis import LDL_analysis
    answer = LDL_analysis(LDL_value)
    assert answer == expected


# def test_user_input(mocker):
#     mocker.patch("builtins.input", 
#                  side_effect=[1, -45])
#     from blood_analysis import user_input
#     answer = user_input()
#     assert answer == False
                 
            