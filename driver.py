# driver.py
# Sophie Davidson 2022 for IMT Atlantique

# Gets experiment info from the user, launches tracker connection with Pupil Labs, then launches the scotoma simulator.

# Imports
import os
import pyglet
import pyautogui
# Modules
from dialogue import launchDialogue
from pupilCaptureAccess import launchConnection
from simulation3D import launchSimulation

# Directory
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)  # Ensure that relative paths start from the same directory as this script

(screenSize) = pyautogui.size()
aprilTagSize = (226, 226)


# Media
tag1Img = pyglet.resource.image("media/tag1.jpg")
tag2Img = pyglet.resource.image("media/tag2.jpg")
tag3Img = pyglet.resource.image("media/tag3.jpg")
tag4Img = pyglet.resource.image("media/tag3.jpg")

tag1 = pyglet.sprite.Sprite(tag1Img, 0, 0)
tag2 = pyglet.sprite.Sprite(tag2Img, 0, screenSize[1] - aprilTagSize[1])
tag3 = pyglet.sprite.Sprite(tag3Img, screenSize[0] - aprilTagSize[1], 0)
tag4 = pyglet.sprite.Sprite(tag4Img, screenSize[0] - aprilTagSize[1], screenSize[1] - aprilTagSize[1])

tags = (tag1, tag2, tag3, tag4)

# Background Image
backgroundImg = pyglet.resource.image("media/background.jpg")
background = pyglet.sprite.Sprite(backgroundImg, 0, 0)
# All Screen Details
screenAttributes = {"AprilTagSize": aprilTagSize,
                    "Background": background,
                    "Tags": tags
                    }


# Main Program ----------------------------------------------------------------------------------
def main():
    response = launchDialogue()
    experimentAttributes = {"name": response[0],
                            "age": response[1],
                            "radius": response[2],
                            "location": response[3],
                            "tracker": response[4],
                            "separation": response[5]}

    sub = None
    if experimentAttributes.get("tracker") == "Pupil Labs Core":
        sub = launchConnection()
    experimentAttributes["sub"] = sub

    launchSimulation(screenAttributes, experimentAttributes)


if __name__ == "__main__":
    main()
