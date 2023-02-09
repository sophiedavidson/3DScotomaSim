
# Imports
import tkinter as tk
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

        # Device: If nothing selected, prompts user to select a device before submitting
        device = device_var.get()
        if device == "Tracker...":
            showMessage("Please select a tracker")
            root.mainloop()

        stimulus = text_entry.get()

        thisInfo = (device, stimulus)

        # close window and return
        root.destroy()

        return input

    # Generating the dialogue window
    root = tk.Tk()
    root.title("Configurations")
    root.geometry("300x100")

    # Select Eye Tracker Drop Down
    device_label = ttk.Label(root, text="Select Tracker")
    device_label.grid(row=3, column=0)
    deviceOptions = ["Tracker...", "Pupil Labs Core Local", "Pupil Labs Core Remote"]
    device_var = tk.StringVar()
    device_var.set("Select A Tracker")
    device_dropdown = ttk.OptionMenu(root, device_var, *deviceOptions)
    device_dropdown.grid(row=3, column=1)

    text_entry_label = ttk.Label(root, text="Text Stimulus")
    text_entry_label.grid(row=4, column=0)
    text_entry = ttk.Entry(root)
    text_entry.grid(row=4, column=1)

    # Submit button
    submit_button = ttk.Button(root, text="Submit", command=get_input)
    submit_button.grid(row=5, column=0)

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
