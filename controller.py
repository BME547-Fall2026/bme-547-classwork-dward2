db = []

# "test": [("HDL", 165), {"LDL", 20)]


def new_patient(patient_name,
                patient_mrn,
                patient_dob):
    patient = {"name": patient_name,
               "mrn": patient_mrn,
               "dob": patient_dob,
               "test": []}
    db.append(patient)
    save_database()
    return "Patient added to database"


def save_database():
    out_file = open("patient_monitor_db.txt",
                    "w")
    for patient in db:
        out_string = "{},{},{}\n".format(
            patient["name"],
            patient["mrn"],
            patient["dob"])
        out_file.write(out_string)
    out_file.close()

    with open("patient_monitor_db.txt", "w") as out_file:
        for patient in db:
            out_string = "{},{},{}\n".format(
                patient["name"],
                patient["mrn"],
                patient["dob"])
            out_file.write(out_string)
    print("done")


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
        if patient["mrn"] == mrn:
            return patient
    return None


def load_tests_into_db():
    # Load in the test file
    all_lines = load_test_file()
    # For each test in file,
    for line in all_lines:
        # Parse the data to get the mrn
        mrn, test_results = parse_test_line(line)
        # Find the correct db entry based mrn
        patient = get_patient_by_mrn(mrn)
        # Add test result to correct patient
        patient["test"].append(test_results)
    print(db)


def initialize():
    all_lines = read_database()
    populate_db(all_lines)
    load_tests_into_db()
    print("Database:")
    print(db)


def get_patients_for_display():
    output_list = []
    for patient in db:
        output_list.append("{} - {}".
                           format(patient["name"],
                                  patient["mrn"]))
    return output_list


def get_patient_by_index(i):
    patient = db[i]
    return (patient["name"],
            patient["mrn"],
            patient["dob"])
