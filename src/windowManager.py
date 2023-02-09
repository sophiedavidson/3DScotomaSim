"""
windowManager.py
Author: Sophie Davidson
Date: 2023

This module manages all functions related to the creation of the stereoscopic window.
"""

import pyglet
from dialogue import showMessage
from pyglet.window import NoSuchConfigException
from pyglet.gl import *


# Get all available screens as a screen object to be used for config
def get_screens():
    display = pyglet.canvas.get_display()
    currentScreen = display.get_screens()

    return currentScreen


# Create the stereoscopic window and return the window object.
def createWindow(isStereoscopic):
    # Configure a stereoscopic display window, warn user if screen could not be created
    screens = get_screens()
    config = Config()
    config.stereo = isStereoscopic
    config.double_buffer = True
    window = None

    try:
        window = pyglet.window.Window(screen=screens[isStereoscopic], config=config, fullscreen=True)
        window.set_caption("Opacity Fusion Test")
    except IndexError:
        showMessage("No secondary screen could be detected")

        quit()
    except NoSuchConfigException:
        showMessage("3D display could not be found, ensure display is 3D compatible")
        quit()

    return window
