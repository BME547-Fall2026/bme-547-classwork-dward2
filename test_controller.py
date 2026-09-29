import pytest


def test_new_patient():
    # Arrange
    from controller import new_patient, db, Patient
    patient_name = "David"
    patient_mrn = 123
    patient_dob = "1/1/11"
    expected = Patient(patient_name,
                       patient_mrn,
                       patient_dob)
    # Act
    answer = new_patient(patient_name, patient_mrn, patient_dob)
    
    # Assert
    assert answer == "Patient added to database"
    assert len(db) == 1
    assert db[0] == expected
                      
                      
def test_add_test_to_patient():
    # Arrange
    from controller import new_patient, add_test_to_patient, db
    db.clear()
    new_patient("Dave", 123, "1/1/11")
    mrn = 123
    test_results= ("HDL", 56)
    # Act
    add_test_to_patient(mrn, test_results)
    # Assert
    from controller import get_patient_by_mrn
    patient = get_patient_by_mrn(mrn)
    assert patient.tests == [("HDL", 56)]
    assert len(db) == 1


def test_Patient_init():
    from controller import Patient
    p_name = "Ann Ables"
    p_mrn = 123
    p_dob = "1/1/1111"
    answer = Patient(p_name, p_mrn, p_dob)
    assert answer.mrn == p_mrn
    assert answer.name == p_name
    assert answer.dob == "1-1-1111"

def test_Patient_calculate_age():
    from controller import Patient
    patient = Patient("Ann Ables", 123, "9/29/2011")
    age = patient.calculate_age()
    assert age == pytest.approx(15, rel=0.1)

