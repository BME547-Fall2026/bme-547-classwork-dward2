db =[]


def new_patient(patient_name,
                patient_mrn,
                patient_dob):
    patient = {"name": patient_name,
               "mrn": patient_mrn,
               "dob": patient_dob}
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
    print(all_lines)
    
    
read_database()
    