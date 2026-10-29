import pytest


def test_Patient_init():
    from database import Patient
    p_name = "Ann Ables"
    p_mrn = 123
    p_dob = "1/1/1111"
    answer = Patient(p_name, p_mrn, p_dob)
    assert answer.mrn == p_mrn
    assert answer.name == p_name
    assert answer.dob == "1-1-1111"


def test_Patient_calculate_age():
    from database import Patient
    patient = Patient("Ann Ables", 123, "9/29/2011")
    age = patient.calculate_age()
    assert age == pytest.approx(15, rel=0.1)
