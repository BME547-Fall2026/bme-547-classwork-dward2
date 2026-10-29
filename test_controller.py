import pytest
import requests_mock
# NOTE:  Logging functionality should also be tested,
#        but not included here


def test_new_patient(requests_mock):
    # Arrange
    from controller import new_patient, server
    patient_name = "David"
    patient_mrn = "123"
    patient_dob = "1/1/2001"
    requests_mock.post(server + "/add_patient",
                       status_code=200,
                       json="Ok")
    # Act
    answer = new_patient(patient_name, patient_mrn, patient_dob)
    # Assert
    assert answer == "Ok"


def test_new_patient_server_error(requests_mock):
    # Arrange
    from controller import new_patient, server
    patient_name = "David"
    patient_mrn = "123"
    patient_dob = "1/1/2001"
    requests_mock.post(server + "/add_patient",
                       status_code=400,
                       text="Error")
    # Act
    answer = new_patient(patient_name, patient_mrn, patient_dob)
    # Assert
    answer = "Error"


def test_new_patient_bad_mrn():
    # Arrange
    from controller import new_patient
    # Act
    answer = new_patient("David", "abc", "1/1/2001")
    # Assert
    assert answer == "MRN must be an integer"
