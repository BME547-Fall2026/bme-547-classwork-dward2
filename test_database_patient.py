# test_database_Patient.py
from database import Patient
import random

mrn = 0


def test_Patient_make_connection():
    Patient.make_connection()
    try:
        Patient.client.admin.command("ping")
        assert True
    except Exception as e:
        assert False


def test_Patient_create():
    global mrn
    mrn = random.randint(1, 1000000000000)
    patient = Patient("One", mrn, "1/1/2001")
    patient.save()
    answer = Patient.collection.find_one({"_id": mrn})
    assert answer is not None
    assert answer["_id"] == mrn
    assert answer["name"] == "One"


def test_Patient_retrieve():
    patient = Patient.find_by_mrn(mrn)
    assert patient is not None
    assert patient.mrn == mrn
    assert patient.name == "One"


def test_Patient_retrieve_not_found():
    patient = Patient.find_by_mrn(0)
    assert patient is None


def test_Patient_update():
    patient = Patient.find_by_mrn(mrn)
    test_result = ["HDL", 50.0]
    patient.tests.append(test_result)
    patient.save()
    answer = Patient.collection.find_one({"_id": mrn})
    assert answer["tests"] == [test_result]


def test_Patient_delete():
    patient = Patient.find_by_mrn(mrn)
    assert patient is not None
    patient.delete()
    answer = Patient.collection.find_one({"_id": mrn})
    assert answer is None
