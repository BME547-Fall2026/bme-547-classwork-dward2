import logging
from mockpatient import MockPatient
import numpy as np
import requests

server = "http://127.0.0.1:5000"


patient_monitor = None
ecg_time = None
ecg_voltage = None


def new_patient(patient_name,
                patient_mrn,
                patient_dob):
    try:
        mrn_number = int(patient_mrn)
    except ValueError:
        logging.error("MRN entered as not an integer")
        return "MRN must be an integer"
    patient_json = {"name": patient_name,
                    "mrn": mrn_number,
                    "dob": patient_dob}
    r = requests.post(server + "/add_patient", json=patient_json)
    if r.status_code == 200:
        logging.info("Patient name {} saved".format(patient_name))
        return r.json()
    else:
        error_message = "Server error: {}".format(r.text)
        logging.error(error_message)
        return error_message


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


def load_tests_into_db():
    # Load in the test file
    all_lines = load_test_file()
    # For each test in file,
    for line in all_lines:
        # Parse the data to get the mrn
        mrn, test_results = parse_test_line(line)
        add_test_to_patient(mrn, test_results)


def add_test_to_patient(mrn, test_results):
    test_json = {"mrn": int(mrn), 
                 "test_name": test_results[0],
                 "test_value": float(test_results[1])}
    r = requests.post(server+"/add_test", json=test_json)
    if r.status_code != 200:
        print("Error adding test")
        print("  Status Code: {}".format(r.status_code))
        print("  Message:  {}".format(r.text))


def initialize():
    logging.basicConfig(filename="gui_controller.log", level=logging.INFO,
                        filemode="w")
    all_lines = read_database()
    populate_db(all_lines)
    load_tests_into_db()


def get_patients_for_display():
    output_list = []
    r = requests.get(server + "/get_all_mrns")
    all_mrns = r.json()
    for mrn in all_mrns:
        r = requests.get(server + "/get_patient/{}".format(mrn))
        patient_info = r.json()
        output_list.append("{} - {}". format(
            patient_info["name"],
            patient_info["mrn"]
        ))
    return output_list


def get_patient_by_index(choice):
    _, p_mrn = choice.split("-")
    mrn = int(p_mrn.strip(" "))
    r = requests.get(server + "/get_patient/{}".format(mrn))
    patient_info = r.json()
    return (patient_info["name"], 
            patient_info["mrn"],
            patient_info["dob"])

def start_patient():
    global patient_monitor
    patient_monitor = MockPatient()


def get_latest_patient_ecg():
    global ecg_time, ecg_voltage
    t, v, _ = patient_monitor.get_data()
    ecg_time = np.append(ecg_time, t)
    ecg_voltage = np.append(ecg_voltage, v)
    return ecg_time, ecg_voltage