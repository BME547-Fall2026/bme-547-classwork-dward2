import pytest


def test_new_patient():
    # Arrange
    from controller import new_patient, db
    patient_name = "David"
    patient_mrn = 123
    patient_dob = "1/1/11"
    # Act
    answer = new_patient(patient_name, patient_mrn, patient_dob)
    
    # Assert
    assert answer == "Patient added to database"
    assert len(db) == 1
    assert db[0] == {"name": patient_name,
                      "mrn": patient_mrn,
                      "dob": patient_dob,
                      "test": []}
                      
                      
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
    assert patient["test"] == [("HDL", 56)]
    assert len(db) == 1
