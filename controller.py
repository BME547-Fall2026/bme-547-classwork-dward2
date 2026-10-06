from datetime import datetime
import logging
from mockpatient import MockPatient
import numpy as np


db = []
patient_monitor = None
ecg_time = None
ecg_voltage = None

# "test": [("HDL", 165), {"LDL", 20)]


class Patient:

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


def new_patient(patient_name,
                patient_mrn,
                patient_dob):
    try:
        mrn_number = int(patient_mrn)
    except ValueError:
        logging.error("MRN entered as not an integer")
        return "MRN must be an integer"
    patient = Patient(patient_name,
                      patient_mrn,
                      patient_dob)
    db.append(patient)
    logging.info("Patient name {} saved".format(patient_name))
    # save_database()
    return "Patient added to database"


# def save_database():
#     out_file = open("patient_monitor_db.txt",
#                     "w")
#     for patient in db:
#         out_string = "{},{},{}\n".format(
#             patient["name"],
#             patient["mrn"],
#             patient["dob"])
#         out_file.write(out_string)
#     out_file.close()

#     with open("patient_monitor_db.txt", "w") as out_file:
#         for patient in db:
#             out_string = "{},{},{}\n".format(
#                 patient["name"],
#                 patient["mrn"],
#                 patient["dob"])
#             out_file.write(out_string)
#     print("done")


def read_database():
    with open("patient_monitor_db.txt", "r") as in_file:
        all_lines = in_file.readlines()
    return all_lines


def populate_db(all_lines):
    for line in all_lines:
        strip_line = line.strip("\n")
        p_name, mrn, dob = strip_line.split(",")
        new_patient(p_name, mrn, dob)


def load_test_file():
    with open("db_test_data.txt", 'r') as in_file:
        all_lines = in_file.readlines()
    return all_lines


def parse_test_line(line):
    mrn, test_name, test_value = line.strip("\n").split(",")
    test_result = (test_name, test_value)
    return mrn, test_result


def get_patient_by_mrn(mrn):
    for patient in db:
        if patient.mrn == mrn:
            return patient
    return None


def load_tests_into_db():
    # Load in the test file
    all_lines = load_test_file()
    # For each test in file,
    for line in all_lines:
        # Parse the data to get the mrn
        mrn, test_results = parse_test_line(line)
        add_test_to_patient(mrn, test_results)
    print(db)


def add_test_to_patient(mrn, test_results):
    # Find the correct db entry based mrn
    print("mrn: {}".format(mrn))
    print("db: {}".format(db))
    patient = get_patient_by_mrn(mrn)
    # Add test result to correct patient
    patient.tests.append(test_results)


def initialize():
    logging.basicConfig(filename="gui_controller.log", level=logging.INFO,
                        filemode="w")
    all_lines = read_database()
    populate_db(all_lines)
    load_tests_into_db()
    print("Database:")
    print(db)
    


def get_patients_for_display():
    output_list = []
    for patient in db:
        output_list.append("{} - {}".
                           format(patient.name,
                                  patient.mrn))
    return output_list


def get_patient_by_index(i):
    patient = db[i]
    return (patient.name,
            patient.mrn,
            patient.dob)


def start_patient():
    global patient_monitor
    patient_monitor = MockPatient()


def get_latest_patient_ecg():
    global ecg_time, ecg_voltage
    t, v, _ = patient_monitor.get_data()
    ecg_time = np.append(ecg_time, t)
    ecg_voltage = np.append(ecg_voltage, v)
    return ecg_time, ecg_voltage


if __name__ == "__main__":
    x = Patient("Ann Ables", 123, "9/29/2011")
    print(x.calculate_age())
    print(x.is_minor())
    print(x.mailing_address())
