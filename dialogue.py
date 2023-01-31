"""
file: dialogue.py
name: Sophie Davidson
company:IMT Atlantique
date: 1/2023

    This module will generate a dialogue box which asks the user for the experiment information, and information about
    the defaults for the simulation.

"""

# Imports
import tkinter as tk
import sys
from tkinter import ttk
from tkinter import messagebox

# Globals
global thisInfo, remoteInfo


# Display a warning message to the user
def showMessage(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Configuration", message)

# ---- Make the Dialogue Box -------------------------------------------------------------------------------------------
def launchDialogue():
    global thisInfo


    def get_input():
        global thisInfo
        # Name: If nothing entered, prompts user to enter a name before submitting
        name = name_entry.get()
        if name == "":
            showMessage("Please enter a name")
            root.mainloop()

        # Age: If nothing entered, prompts user to enter a age before submitting
        age = age_entry.get()
        if age == "":
            showMessage("Please enter an age")
            root.mainloop()

        # Device: If nothing selected, prompts user to select a device before submitting
        device = device_var.get()
        if device == "Tracker...":
            showMessage("Please select a tracker")
            root.mainloop()

        # scotoma radius: If nothing entered, or value not a number, prompts user to enter a radius before submitting
        try:
            scotoma = int(scotoma_entry.get())

        except ValueError:
            showMessage("Please enter a integer value for scotoma radius")
            root.mainloop()

        # location: if no location selected, prompts user to enter a radius before submitting
        location = location_var.get()
        if location == "Location...":
            showMessage("Please enter a location")
            root.mainloop()

        # offset: if no offset entered, or not an integer value, prompts user to enter.
        try:
            offset = int(offset_entry.get())
        except ValueError:
            showMessage("Please enter a numerical value for offset")
            root.mainloop()

        # collate all
        thisInfo = (name, age, scotoma, location, device, offset)

        # close window and return
        root.destroy()

        return input

    # Generating the dialogue window
    root = tk.Tk()
    root.title("Configurations")
    root.geometry("300x280")

    experiment_details = ttk.Label(root, text="Experiment Details\n")
    experiment_details.grid(row=0, column=0)

    # Name label and entry
    name_label = ttk.Label(root, text="Name:")
    name_label.grid(row=1, column=0)
    name_entry = ttk.Entry(root)
    name_entry.grid(row=1, column=1)

    # Age label and entry
    age_label = ttk.Label(root, text="Age:")
    age_label.grid(row=2, column=0)
    age_entry = ttk.Entry(root)
    age_entry.grid(row=2, column=1)

    # Select Eye Tracker Drop Down
    device_label = ttk.Label(root, text="Select Tracker")
    device_label.grid(row=3, column=0)
    deviceOptions = ["Tracker...", "Pupil Labs Core Local", "Pupil Labs Core Remote", "Mouse"]
    device_var = tk.StringVar()
    device_var.set("Select A Tracker")
    device_dropdown = ttk.OptionMenu(root, device_var, *deviceOptions)
    device_dropdown.grid(row=3, column=1)

    experiment_details = ttk.Label(root, text="\nScotoma Details\n")
    experiment_details.grid(row=4, column=0)

    # Select Eye Tracker Drop Down
    location_label = ttk.Label(root, text="Select Location:")
    location_label.grid(row=5, column=0)
    locationOptions = ["Location...", "N", "E", "S", "W", "Central"]
    location_var = tk.StringVar()
    location_var.set("Select a Location")
    location_dropdown = ttk.OptionMenu(root, location_var, *locationOptions)
    location_dropdown.grid(row=5, column=1)

    # Scotoma Radius label and entry
    scotoma_label = ttk.Label(root, text="Scotoma Radius:")
    scotoma_label.grid(row=6, column=0)
    scotoma_entry = ttk.Entry(root)
    scotoma_entry.grid(row=6, column=1)

    # offset label and entry
    offset_label = ttk.Label(root, text="Offset:")
    offset_label.grid(row=7, column=0)
    offset_entry = ttk.Entry(root)
    offset_entry.grid(row=7, column=1)

    # Submit button
    # TODO - When you click submit, should type and error check and inform user.
    submit_button = ttk.Button(root, text="Submit", command=get_input)
    submit_button.grid(row=8, column=0)

    root.mainloop()

    try:
        return thisInfo  # thisInfo contains (name, age, scotomaRadius, location, tracker, offset)
    except NameError:
        showMessage("Window Closed, Quitting Application")
        exit()


# Defines a separate dialogue to display if the user selects the Remote Option.
def dialogueRemote():
    global remoteInfo
    # Default
    remoteInfo = ("127.0.0.1", "50020")

    # Collect information from the dialogue form.
    def get_input():
        global remoteInfo
        remoteInfo = (ip_entry.get(), port_entry.get())
        root.destroy()
        return input

    # Generate dialogue window
    root = tk.Tk()
    root.title("Remote Configuration")
    root.geometry("400x280")

    details = ttk.Label(root,
                        text="Please open pupil capture Network API settings."
                        "\nUnder the 'connect remotely' heading "
                        "the address should be provided as:"
                        "\n'tcp://IP_ADDRESS:PORT",
                        justify="center")

    details.grid(row=0, column=0)

    # ip label and entry
    ip_label = ttk.Label(root, text="IP Address:")
    ip_label.grid(row=1, column=0)
    ip_entry = ttk.Entry(root)
    ip_entry.grid(row=2, column=0)

    # port label and entry
    port_label = ttk.Label(root, text="Port:")
    port_label.grid(row=3, column=0)
    port_entry = ttk.Entry(root)
    port_entry.grid(row=4, column=0)

    # When submit button is clicked, collect the inputs.
    submit_button = ttk.Button(root, text="Submit", command=get_input)
    submit_button.grid(row=8, column=0)

    root.mainloop()

    return remoteInfo
