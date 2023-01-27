# dialogue.py
# Created by Sophie Davidson for IMT Atlantique, 2022

# This module will create a dialogue box to determine key information about the participant and experiment.
import tkinter as tk
from tkinter import ttk

# ---- Make the Dialogue Box ---------------------------------------------------

global thisInfo, remoteInfo


def launchDialogue():
    thisInfo = ("Default", 0, 50, "Central", "Mouse", 5)

    def get_input():
        global thisInfo
        name = name_entry.get()
        age = age_entry.get()
        device = device_var.get()
        scotoma = scotoma_entry.get()
        location = location_var.get()
        offset = offset_entry.get()
        thisInfo = (name, age, int(scotoma), location, device, int(offset))
        root.destroy()
        return input

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

    return thisInfo  # thisInfo contains (name, age, scotomaRadius, location, tracker, offset)


def dialogueRemote():
    remoteInfo = ("127.0.0.1", "50020")

    def get_input():
        global remoteInfo
        remoteInfo = (ip_entry.get(), port_entry.get())
        root.destroy()
        return input

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

    submit_button = ttk.Button(root, text="Submit", command=get_input)
    submit_button.grid(row=8, column=0)

    root.mainloop()

    return remoteInfo
