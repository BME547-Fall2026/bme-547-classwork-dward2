import pytest
from server import app
from database import db

client = app.test_client()


def test_server_status():
    r = client.get("/")
    assert r.status_code == 200
    assert r.text == "Patient Monitoring Server is On"


def test_post_add_patient():
    # Arrange
    db.clear()
    in_json = {"name": "David Ward",
               "mrn": 123,
               "dob": "1/21/2001"}
    # Act
    r = client.post("/add_patient", json=in_json)
    # Assert
    assert len(db) == 1
    assert db[0].name == "David Ward"
    assert r.status_code == 200
    assert r.get_json() == "Patient MRN=123 added to database"
    # The `r` response class returned by the Flask.test_client() is
    #   not the exact same response class as returned by the
    #   `requests` package.  One difference:  to get the JSON decoded
    #   response, you need to use `r.get_json()` instead of `r.json()`.


def test_post_add_patient_bad_request():
    # Arrange
    db.clear()
    in_json = {"name": "David Ward",
               "mrn": 123}
    # Act
    r = client.post("/add_patient", json=in_json)
    # Assert
    assert len(db) == 0
    assert r.status_code == 400
    assert r.text == "Key dob is missing"


@pytest.mark.parametrize("in_data, expected, ex_answer", [
    (["hello"], {"one": int}, "JSON data needs to be a dictionary."),
    ({"one": 15, "two": "hello"}, {"one": int, "two": str}, True),
    ({"one": 15, "three": "good"}, {"one": int, "two": str},
     "Key two is missing"),
    ({"one": 15, "two": 15}, {"one": int, "two": str},
     "Key two value is not <class 'str'>")
])
def test_generic_validate_input(in_data, expected, ex_answer):
    from server import generic_validate_input
    answer = generic_validate_input(in_data, expected)
    assert answer == ex_answer


def setup_patient():
    """
    Function to set up a patient for remaining tests
    """
    db.clear()
    in_json = {"name": "Ann Ables",
               "mrn": 234,
               "dob": "2/2/2002"}
    r = client.post("/add_patient", json=in_json)


def test_get_get_patient():
    # Arrange
    setup_patient()
    # Act
    r = client.get("/get_patient/234")
    # Assert
    assert r.status_code == 200
    assert r.get_json() == {"name": "Ann Ables",
                            "mrn": 234,
                            "dob": "2-2-2002",
                            "tests": []}


def test_get_get_patient_bad_mrn():
    # Arrange
    setup_patient()
    # Act
    r = client.get("/get_patient/345")
    # Assert
    assert r.status_code == 400
    assert r.text == "MRN of 345 does not exist"


@pytest.mark.parametrize("mrn, expected", [
    ("234", 234),
    ("23.4", "MRN must be an integer"),
    ("234ABC", "MRN must be an integer"),
    ("345", "MRN of 345 does not exist")
])
def test_validate_get_patient_mrn(mrn, expected):
    # Arrange
    from server import validate_get_patient_mrn
    setup_patient()
    # Act
    answer = validate_get_patient_mrn(mrn)
    # Assert
    assert answer == expected


def test_post_add_test():
    # Arrange
    setup_patient()
    lab_data = {"mrn": 234, "test_name": "HDL", "test_value": 23.0}
    # Act
    r = client.post("/add_test", json=lab_data)
    # Assert
    assert r.status_code == 200
    assert len(db[0].tests) == 1
    assert db[0].tests == [("HDL", 23.0)]


def test_post_add_test_bad_validation():
    # Arrange
    setup_patient()
    lab_data = [234, "HDL", 23.6]
    # Act
    r = client.post("/add_test", json=lab_data)
    # Assert
    assert r.status_code == 400
    assert r.text == "JSON data needs to be a dictionary."
    assert len(db[0].tests) == 0


def test_post_add_test_missing_mrn():
    # Arrange
    setup_patient()
    lab_data = {"mrn": 345, "test_name": "HDL", "test_value": 23.0}
    # Act
    r = client.post("/add_test", json=lab_data)
    # Assert
    assert r.status_code == 400
    assert r.text == "MRN of 345 does not exist"
