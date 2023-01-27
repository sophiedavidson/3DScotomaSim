# dialogue.py
# Created by Sophie Davidson for IMT Atlantique, 2022

# This module will create a dialogue box to determine key information about the participant and experiment.

# ---- Make the Dialogue Box ---------------------------------------------------

# TODO - Find psychopy alternative for dialogue and implement here.
def launchDialogue():
    name = input("Name: ")
    age = input("Age: ")
    scotomaRadius = int(input("Scotoma Radius: "))
    trackerType = int(input("type 1 for Mouse, type 2 for eyetracker: "))
    if trackerType == 1:
        tracker = "Mouse"
    else:
<<<<<<< Updated upstream
        print('User cancelled')  # ...or False, if they hit Cancel

    """
    thisInfo = ("Sophie", "20", 50, "Central","Pupil Labs Core", 15 )
=======
        tracker = "Pupil Labs Core"
    offset = int(input("Offset: "))
>>>>>>> Stashed changes

    thisInfo = (name, age, scotomaRadius, "Central", tracker, offset)
    return thisInfo  # thisInfo contains (name,age,scotoma radius, location, tracker, offset)
