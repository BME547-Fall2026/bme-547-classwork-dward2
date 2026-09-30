def import_file_info():
    patient_list = ["Patient 1", "Patient 2", "Patient 3"]
    hospital_list = ["Grace Memorial", "Methodist", "Memorial City",
                     "St. Luke's Episcopal", "M.D. Anderson",
                     "Ben Taub County", "Cypress Creek", "Katy Memorial"]
    with open("data_ex2.txt", 'r') as in_file:
        med_data = in_file.readlines()
    medicine_list = [x.strip("\n") for x in med_data]
    list_1 = length_of_list(patient_list)
    list_2 = length_of_list(hospital_list)
    list_3 = length_of_list(medicine_list)

    return patient_list, list_1, hospital_list, list_2, medicine_list, list_3


def length_of_list(list_to_check):
    return len(list_to_check)

def setup_database():
    pass

def initialize_log_file():
    pass

