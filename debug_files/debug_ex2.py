
def define_things():
    import database_config
    global database
    db = database_config.setup_database()
    global patient_list, hospital_list, medicine_list
    global l1, l2, l3
    patient_list, l1, hospital_list, l2, medicine_list, l3 = \
        database_config.import_file_info()
    database_config.initialize_log_file()


def output_hospital_list(hospital_list):
    print("This is the list of participating hospitals")
    for i, hospital in enumerate(hospital_list):
        print("{}: {}".format(i, hospital))
    print("\n")
    return


def output_patient_list(patient_list):
    print("This is the list of participating patients")
    for i, patient in enumerate(patient_list):
        print("{}: {}".format(i, patient))
    print("\n")
    return


def read_in_data(filename):
    out_list = list()
    with open(filename, 'r') as in_file:
        x = in_file.readlines()
        for line in x:
            out_list.append(line.strip("\n"))
    return out_list


def output_results(dataset):
    k = 0
    while k < l3:
        med_name = dataset[k]
        print("{}: {}".format(k, med_name))
        k += 1
    pass


if __name__ == '__main__':
    define_things()
    dataset_2 = read_in_data("data_ex2.txt")
    output_results(dataset_2)
    print("End program")
