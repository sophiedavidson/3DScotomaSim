"""
file: driver.py
name: Sophie Davidson
company:IMT Atlantique
date: 1/2023

    The following module is the main driver for the program. The driver controls the sequential launching of screens.
    First, the program collects the experimental information by calling launchDialogue, then depending on trackerType
    selected, a second remote-connection dialogue may be shown. Then the connection is launched with the selected
    tracker, and the 3D simulation is launched.

"""

# Imports
import os
import pyglet
from dialogue import launchDialogue, dialogueRemote
from pupilCaptureAccess import launchConnection
from simulation3D import launchSimulation


# Directory Information
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)  # Ensure that relative paths start from the same directory as this script

# Constants
screenSize = (1280, 720)
aprilTagSize = (226, 226)

# Media
tag1Img = pyglet.resource.image("media/tag1.jpg")
tag2Img = pyglet.resource.image("media/tag2.jpg")
tag3Img = pyglet.resource.image("media/tag3.jpg")
tag4Img = pyglet.resource.image("media/tag4.jpg")

tag1 = pyglet.sprite.Sprite(tag1Img, 0, 0)
tag2 = pyglet.sprite.Sprite(tag2Img, 0, screenSize[1] - aprilTagSize[1])
tag3 = pyglet.sprite.Sprite(tag3Img, screenSize[0] - aprilTagSize[1], 0)
tag4 = pyglet.sprite.Sprite(tag4Img, screenSize[0] - aprilTagSize[1], screenSize[1] - aprilTagSize[1])

tags = (tag1, tag2, tag3, tag4)

# Background Image
backgroundImg = pyglet.resource.image("media/background.png")
background = pyglet.sprite.Sprite(backgroundImg, 0, 0)

# Collating all screen details
screenAttributes = {"ScreenSize": screenSize,
                    "AprilTagSize": aprilTagSize,
                    "Background": background,
                    "Tags": tags
                    }


# Main Program ----------------------------------------------------------------------------------
def main():
    testing = int(input("Enter 1 for testing mode, enter 0 for regular"))
    if testing:
        response = ("Sophie", "20", 100, "Central", "Pupil Labs Core Remote",10)
    else:
        response = launchDialogue()  # collect experiment information from user
    # Collated experiment information
    experimentAttributes = {"name": response[0],
                            "age": response[1],
                            "radius": response[2],
                            "location": response[3],
                            "tracker": response[4],
                            "separation": response[5]}
    # if the trackers selected is remote, collect ip and port details
    if testing:
        remoteDetails = ("172.20.10.2", "50020")
        experimentAttributes["remoteDetails"] = remoteDetails

    else:
        if experimentAttributes.get("tracker") == "Pupil Labs Core Remote":
            remoteDetails = dialogueRemote()
            experimentAttributes["remoteDetails"] = remoteDetails

    # if the tracker is an eyetracker, launch the connection to the eyetracker.
    if experimentAttributes.get("tracker") == "Pupil Labs Core Local" or "Pupil Labs Core Remote":
        sub = launchConnection(experimentAttributes)
        experimentAttributes["sub"] = sub

    # launch the simulation
    launchSimulation(screenAttributes, experimentAttributes)


if __name__ == "__main__":
    main()
