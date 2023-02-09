"""
driver.py
Author: Sophie Davidson
Date: 2023

The driver loads all the required media, gets the user's experimental setup requirements, launches the pupil capture
connection and then launches the scotoma simulator.

"""
# Imports
import os
import pyglet
# Modules
from dialogue import launchDialogue, dialogueRemote
from pupilCaptureAccess import launchConnection
from simulation3D import launchSimulation

# Directory
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)  # Ensure that relative paths start from the same directory as this script

screenSize = (1280, 720)
aprilTagSize = (226, 226)

# Media
tag1Img = pyglet.resource.image("media/tag1.jpg")
tag2Img = pyglet.resource.image("media/tag2.jpg")
tag3Img = pyglet.resource.image("media/tag3.jpg")
tag4Img = pyglet.resource.image("media/tag4.jpg")

# Turn images into modifiable "sprite" objects to make handling easier
tag1 = pyglet.sprite.Sprite(tag1Img, 0, 0)
tag2 = pyglet.sprite.Sprite(tag2Img, 0, screenSize[1] - aprilTagSize[1])
tag3 = pyglet.sprite.Sprite(tag3Img, screenSize[0] - aprilTagSize[1], 0)
tag4 = pyglet.sprite.Sprite(tag4Img, screenSize[0] - aprilTagSize[1], screenSize[1] - aprilTagSize[1])

tags = (tag1, tag2, tag3, tag4)


# All Screen Details
screenAttributes = {"ScreenSize": screenSize,
                    "AprilTagSize": aprilTagSize,
                    "Tags": tags
                    }


# Main Program ----------------------------------------------------------------------------------
def main():
    # Ask for the tracker type ie remote or local
    (tracker,stimulus) = launchDialogue()
    experimentAttributes = {"tracker": tracker,
                            "stimulus": stimulus}

    # If remote, get IP and port details, and launch the connection
    if experimentAttributes.get("tracker") == "Pupil Labs Core Remote":
        remoteDetails = dialogueRemote()
        sub = launchConnection(remoteDetails)
        experimentAttributes["sub"] = sub
    # If local, use defaults, and launch connection
    if experimentAttributes.get("tracker") == "Pupil Labs Core Local":
        localDetails = ("127.0.0.1", "50020")
        sub = launchConnection(localDetails)
        experimentAttributes["sub"] = sub

    # run the simulation using the defined parameters
    launchSimulation(screenAttributes, experimentAttributes)


if __name__ == "__main__":
    main()
