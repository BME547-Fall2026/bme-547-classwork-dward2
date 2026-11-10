from datetime import datetime
from pymongo import MongoClient


class Patient:

    client = None
    database = None
    collection = None

    @classmethod
    def make_connection(cls):
        uri = "mongodb+srv://bme547_class:db_demo@bme547.ba348.mongodb.net/"
        cls.client = MongoClient(uri)
        cls.database = cls.client["db_demo"]
        cls.collection = cls.database["Patient"]

    def __init__(self, p_name, p_mrn, p_dob):
        self.name = p_name
        self.mrn = p_mrn
        p_dob = p_dob.replace("/", "-")
        self.dob = p_dob
        self.tests = []

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        if self.mrn != other.mrn:
            return False
        if self.name != other.name:
            return False
        if self.dob != other.dob:
            return False
        if self.tests != other.tests:
            return False
        return True

    def __repr__(self):
        return "Patient: {}, {}, {}".format(self.mrn,
                                            self.name,
                                            self.tests)

    def calculate_age(self):
        birth_date = datetime.strptime(
            self.dob, "%m-%d-%Y")
        today = datetime.now()
        age = today - birth_date
        years = age.days/365
        return round(years, 1)

    def is_minor(self):
        age = self.calculate_age()
        if age < 18:
            return True
        else:
            return False

    def output_dict(self):
        out_dict = {"name": self.name,
                    "mrn": self.mrn,
                    "dob": self.dob,
                    "tests": self.tests}
        return out_dict

    def save(self):
        document = self.collection.find_one({"_id": self.mrn})
        mongo = {"_id": self.mrn,
                 "name": self.name,
                 "dob": self.dob,
                 "tests": self.tests}
        if document is None:
            result = self.collection.insert_one(mongo)
        else:
            result = self.collection.replace_one({"_id": self.mrn}, mongo)
        return result

    def delete(self):
        return self.collection.delete_one({"_id": self.mrn})

    @classmethod
    def find_by_mrn(cls, mrn):
        item = cls.collection.find_one({"_id": mrn})
        if item is None:
            return None
        mrn = item["_id"]
        p_name = item["name"]
        dob = item["dob"]
        tests = item["tests"]
        new_patient = Patient(p_name, mrn, dob)
        new_patient.tests = tests
        return new_patient

    @classmethod
    def get_all_mrns(cls):
        mrns = cls.collection.distinct("_id")
        return mrns

    @classmethod
    def clear_database(cls):
        cls.collection.delete_many({})


def process_new_patient(in_data):
    new_patient = Patient(in_data["name"],
                          in_data["mrn"],
                          in_data["dob"])
    new_patient.save()
    return "Patient MRN={} added to database".format(in_data["mrn"])


def get_patient_by_mrn(mrn):
    patient = Patient.find_by_mrn(mrn)
    return patient


def get_patient_for_server(mrn):
    patient = get_patient_by_mrn(mrn)
    if patient is not None:
        return patient.output_dict()
    else:
        return None


def add_test_to_patient(mrn, test_name, test_value):
    patient = get_patient_by_mrn(mrn)
    patient.tests.append((test_name, test_value))
    patient.save()
    return "Added test"


def get_all_mrns():
    all_mrns = Patient.get_all_mrns()
    return all_mrns
