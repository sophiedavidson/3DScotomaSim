"""
file: windowManagement.py
name: Sophie Davidson
company:IMT Atlantique
date: 1/2023

    This module contains the functions required to generate a 3D stereoscopic window including the detection of existing
    screens. 

"""

import pyglet
from pyglet.window import NoSuchConfigException
from dialogue import showMessage
from pyglet.gl import *


# Get all available screens as a screen object to be used for config
def get_screens():
    display = pyglet.canvas.get_display()
    currentScreen = display.get_screens()

    return currentScreen


# Configure a stereoscopic display window, warn user if screen could not be created
def createWindow(isStereoscopic):
    screens = get_screens()
    config = Config()
    config.stereo = isStereoscopic
    config.double_buffer = True
    window = None

    try:
        # note that if isStereoscopic, tries to display on secondary screen ([1])
        window = pyglet.window.Window(screen=screens[isStereoscopic], config=config, fullscreen=True)
        window.set_caption("Opacity Fusion Test")

    except IndexError:
        showMessage("No secondary screen could be detected")
        quit()

    except NoSuchConfigException:
        showMessage("3D display could not be found, ensure display is 3D compatible")
        quit()

    # If the window has been successfully made, return the window.
    return window
