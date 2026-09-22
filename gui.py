import tkinter as tk
from tkinter import ttk
import controller

text_font = ("Arial", 24)
status_font = ("Arial", 14)


def main_window():

    def submit_btn_cmd():
        # Get needed data from the GUI
        patient_name = name_value.get()
        patient_mrn = mrn_value.get()
        patient_dob = dob_value.get()
        # Call another function to do the work and get answer
        answer = controller.new_patient(patient_name,
                                        patient_mrn,
                                        patient_dob)
        # Update the GUI with answer as needed
        status_label.configure(text=answer)

    def load_combobox_cmd():
        # Get needed data from the GUI
        # Call another function to do the work
        values = controller.get_patients_for_display()
        # Update GUI as needed
        patient_select.configure(values=values)

    def load_patient_btn_cmd():
        # Get needed data from the GUI
        db_number = patient_select.current()
        # Call another function to do the work
        patient_name, patient_mrn, patient_dob = \
            controller.get_patient_by_index(db_number)
        # Update GUI as needed
        name_value.set(patient_name)
        mrn_value.set(patient_mrn)
        dob_value.set(patient_dob)

    root = tk.Tk()
    root.title("Patient Monitor")
    root.geometry("800x500")

    # Data Frame
    data_frame = tk.Frame(root,
                          borderwidth=2,
                          relief="groove")
    data_frame.grid(column=0, row=0, sticky=tk.N)

    title_label = tk.Label(data_frame,
                           text="Data Frame Placeholder",
                           font=text_font)
    title_label.grid(column=0, row=0)

    # Patient Frame
    patient_frame = tk.Frame(root,
                             borderwidth=2,
                             relief="groove")
    patient_frame.grid(column=1, row=0)

    name_label = tk.Label(patient_frame, text="Name:",
                          font=text_font)
    name_label.grid(column=0, row=0, sticky=tk.E)
    name_value = tk.StringVar()
    name_entry = tk.Entry(patient_frame, font=text_font,
                          textvariable=name_value)
    name_entry.grid(column=1, row=0)

    mrn_label = tk.Label(patient_frame, text="MRN:",
                         font=text_font)
    mrn_label.grid(column=0, row=1, sticky=tk.E)
    mrn_value = tk.StringVar()
    mrn_entry = tk.Entry(patient_frame, font=text_font,
                         textvariable=mrn_value)
    mrn_entry.grid(column=1, row=1)

    dob_label = tk.Label(patient_frame, text="DOB:",
                         font=text_font)
    dob_label.grid(column=0, row=2, sticky=tk.E)
    dob_value = tk.StringVar()
    dob_entry = tk.Entry(patient_frame, font=text_font,
                         textvariable=dob_value)
    dob_entry.grid(column=1, row=2)

    submit_btn = tk.Button(patient_frame, text="Submit",
                           font=text_font,
                           command=submit_btn_cmd)
    submit_btn.grid(column=0, row=3)

    status_label = tk.Label(root, font=status_font)
    status_label.grid(column=0, row=1, sticky=tk.W)

    # Selection Frame
    selection_frame = tk.Frame(root,
                               borderwidth=2,
                               relief="groove")
    selection_frame.grid(column=1, row=1)
    selection_title_label = tk.Label(selection_frame,
                                     text="Select a Patient",
                                     font=text_font)
    selection_title_label.grid(column=0, row=0)

    patient_select = ttk.Combobox(selection_frame,
                                  postcommand=load_combobox_cmd,
                                  font=text_font)
    patient_select.grid(column=0, row=1)

    load_patient_btn = tk.Button(selection_frame,
                                 text="Load Patient",
                                 font=text_font,
                                 command=load_patient_btn_cmd)
    load_patient_btn.grid(column=0, row=2)

    root.mainloop()

    print("End")


if __name__ == "__main__":
    print("Start")
    controller.initialize()
    main_window()
