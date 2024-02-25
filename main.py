"""
MIT License

Copyright (c) 2024 M6r3k

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import tkinter as tk
from datetime import datetime


def compare_master_and_unit(master_carton, unit_labels):
    clear_result_frame()  # Clear previous results

    # Extract the first value of the master carton code
    master_values = master_carton.split(";")
    master_code_first_value = master_values[0]

    # Get current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create the report file with a unique name including the master code value
    report_file_name = f"{master_code_first_value}_report_{current_datetime}.txt"

    with open(report_file_name, "w") as report_file:
        report_file.write("Comparison Report\n")
        report_file.write("Date and Time: {}\n".format(current_datetime))
        report_file.write("Master Carton Code: {}\n".format(master_carton))
        report_file.write("---------------------------------------------------\n")

        for index, unit_box_label in enumerate(unit_labels, start=1):
            unit_values = unit_box_label.split(";")

            if unit_values[0] == master_values[0] and unit_values[1] == master_values[2] and unit_values[
                2] in master_values:
                result = f"{index}. {unit_box_label}: Match found! Legacy Master Carton\n"
            elif unit_values[0] == master_values[0] and unit_values[1] == master_values[1] and unit_values[
                3] in master_values:
                result = f"{index}. {unit_box_label}: Match found! PRO-SIX Master Carton\n"
            else:
                result = f"{index}. {unit_box_label}: No match found.\n"

            # Write result to report file
            report_file.write(result)

            # Display result in GUI
            result_label = tk.Label(result_frame, text=result.strip(), bg="green" if "Match found" in result else "red",
                                    fg="white", anchor=tk.W)
            result_label.pack(fill=tk.X)
            result_widgets.append(result_label)


def submit():
    clear_result_frame()  # Clear previous results
    master_carton_input = master_carton_entry.get()
    unit_labels_input = unit_labels_entry.get("1.0", tk.END).strip().split("\n")
    compare_master_and_unit(master_carton_input, unit_labels_input)


def clear_result_frame():
    for widget in result_widgets:
        widget.destroy()
    result_widgets.clear()


root = tk.Tk()
root.title("Master Carton Comparison")

master_carton_label = tk.Label(root, text="Enter 2D code from Master carton:")
master_carton_label.pack()

master_carton_entry = tk.Entry(root, width=50)
master_carton_entry.pack()

unit_labels_label = tk.Label(root, text="Enter 2D code from Unit labels (one per line):")
unit_labels_label.pack()

unit_labels_entry = tk.Text(root, height=5, width=50)
unit_labels_entry.pack()

button_frame = tk.Frame(root)
button_frame.pack()

submit_button = tk.Button(button_frame, text="Submit", command=submit)
submit_button.pack(side=tk.LEFT)

clear_button = tk.Button(button_frame, text="Clear", command=clear_result_frame)
clear_button.pack(side=tk.LEFT)

result_frame = tk.Frame(root)  # Create result frame
result_frame.pack(fill=tk.X)

result_widgets = []

root.mainloop()
