import tkinter as tk


def main_window():
    root = tk.Tk()

    my_label = tk.Label(root, text="My GUI", foreground="red")
    my_label.grid(column=0, row=0)

    second_label = tk.Label(root, text="Second Label in column 2",
                            wraplength=10)
    second_label.grid(column=3, row=7)

    root.mainloop()

    print("End")


if __name__ == "__main__":
    print("Start")
    main_window()
