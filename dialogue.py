# dialogue.py
# Created by Sophie Davidson for IMT Atlantique, 2022

# This module will create a dialogue box to determine key information about the
# participant and the experiment parameters.
#import psychopy
#from psychopy import gui

# ---- Defaults------------------------------------------------------------------
name = "New Participant"
age = 0
scotomaRadius = 50
scotomaLocation = "Central"
tracker = "Mouse"


# ---- Make the Dialogue Box ---------------------------------------------------

def launchDialogue():
    """
    # Create Dialogue
    dlg = gui.Dlg(title="Experiment Information", pos=(200, 400))
    # participant information
    dlg.addText('Participant Information', color='Blue')
    dlg.addField('Name:', initial=name, tip='Your Full Name')
    dlg.addField('Age:', age)
    # experiment parameters
    dlg.addText('Experiment Parameters', color='Blue')
    dlg.addField('Scotoma Radius:', scotomaRadius)
    dlg.addField('Scotoma Location:', choices=["Central", "N", "NE", "E", "SE", "S", "SW", "W", "NW"],
                 initial=scotomaLocation)
    dlg.addField("Select Tracker:", choices=["Mouse", "Pupil Labs Core"], initial=tracker)
    dlg.addField("Separation:", choices=[0, 5, 10, 15, 20, 25])

    # Call show() to show the dlg and wait for it to close
    thisInfo = dlg.show()

    # button controls
    if dlg.OK:  # This will be True if user hit OK...
        pass
    else:
        print('User cancelled')  # ...or False, if they hit Cancel

    """
    thisInfo = ("Sophie", "20", 50, "Central","Mouse", 5 )

    return thisInfo  # thisInfo contains (name,age,scotoma radius, location, tracker)
