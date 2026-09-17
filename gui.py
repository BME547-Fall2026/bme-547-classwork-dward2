import tkinter as tk
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
    
    root = tk.Tk()
    root.title("Patient Monitor")
    root.geometry("800x500")

    data_frame = tk.Frame(root,
                          borderwidth=2,
                          relief="groove")
    data_frame.grid(column=0, row=0, sticky=tk.N)
    
    title_label = tk.Label(data_frame, 
                           text="Data Frame Placeholder",
                           font=text_font)
    title_label.grid(column=0, row=0)
    
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

    root.mainloop()

    print("End")


if __name__ == "__main__":
    print("Start")
    main_window()
