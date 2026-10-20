db = []


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

    def output_dict(self):
        out_dict = {"name": self.name,
                    "mrn": self.mrn,
                    "dob": self.dob,
                    "tests": self.tests}
        return out_dict


def process_new_patient(in_data):
    new_patient = Patient(in_data["name"],
                          in_data["mrn"],
                          in_data["dob"])
    db.append(new_patient)
    print(db)
    return "Patient MRN={} added to database".format(in_data["mrn"])


def get_patient_by_mrn(mrn):
    for patient in db:
        if patient.mrn == mrn:
            return patient
    return None


def get_patient_for_server(mrn):
    patient = get_patient_by_mrn(mrn)
    if patient is not None:
        return patient.output_dict()
    else:
        return None


def add_test_to_patient(mrn, test_name, test_value):
    patient = get_patient_by_mrn(mrn)
    patient.tests.append((test_name, test_value))
    return "Added test"
