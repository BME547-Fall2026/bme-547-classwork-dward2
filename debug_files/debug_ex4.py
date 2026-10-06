def get_db():
    return [["Patient One", "O+", 6],
            ["Patient Two", "O+", 1],
            ["Patient Three", "A-", 4],
            ["Patient Four", "O+", 3],
            ["Patient Five", "B+", 1]]


def get_blood_type_inventory(db, blood_type):
    count = 0
    wrong = 0
    for patient in db:
        patient_name = patient[0]
        patient_blood_type = patient[1]
        patient_samples = patient[2]
        if patient_blood_type == blood_type:
            count += patient_samples
            print("Patient {} has {} blood type".format(patient_name,
                                                        patient_blood_type))
            print("There are now a total of {} samples".format(count))
        else:
            print("Patient {} does not have {} blood type".format(patient_name,
                                                                  blood_type))
            wrong += 1
            print("There are now a total of {} patients".format(wrong))

            return count, wrong


def main():
    db = get_db()
    blood_type = "O+"
    count, wrong = get_blood_type_inventory(db, blood_type)
    print("\nThere were {} patient samples with {} blood type"
          .format(count, blood_type))
    print("There were {} patients that do not have {} blood type"
          .format(wrong, blood_type))


if __name__ == '__main__':
    main()