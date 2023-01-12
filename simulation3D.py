# simulation.py
# Sophie Davidson for IMT Atlantique, 2022

# The following module generates the main screen of the program, including
# the April Tag Markers to be used for configuration of the device, and the
# simulated scotoma over a text background.

# Imports
import pyglet
import tkinter as tk
from tkinter import messagebox
from pyglet.gl import *
from pyglet.window import NoSuchConfigException
from pyglet import shapes
from pupilCaptureAccess import getGazePosition


def showMessage(message):
    # Display a warning message to the user
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Configuration", message)


def get_screens():
    # Get all available screens as a screen object to be used for config
    display = pyglet.canvas.get_display()
    currentScreen = display.get_screens()

    return currentScreen


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


# Moves the scotoma to a relative location.
def transformEyeData(x, y, location):
    if location == "N":
        y = y - 50
    elif location == "NE":
        x = x + 50
        y = y - 50
    elif location == "E":
        x = x + 50
    elif location == "SE":
        x = x + 50
        y = y + 50
    elif location == "S":
        y = y + 50
    elif location == "SW":
        x = x - 50
        y = y + 50
    elif location == "W":
        x = x - 50
    elif location == "NW":
        x = x - 50
        y = y - 50
    return x, y


# Draws the april tags
def drawTags(screenAttributes):
    # get required attributes
    tags = screenAttributes.get("Tags")

    tags[0].draw()
    tags[1].draw()
    tags[2].draw()
    tags[3].draw()


# Draws all of the foreground components
def drawAll(x, y, screenAttributes, experimentAttributes):
    # get details required

    screen = screenAttributes.get("Screen")
    background = screenAttributes.get("Background")
    scotomaRadius = experimentAttributes.get("radius")
    separation = experimentAttributes.get("separation")

    # clear screen
    glClearColor(1, 1, 1, 1)
    glDrawBuffer(GL_BACK_LEFT)
    glClear(GL_COLOR_BUFFER_BIT)
    (x1, y1) = transformEyeData(x, y, experimentAttributes.get("location"))
    scotomaLeft = shapes.Circle(x1, y1, scotomaRadius, color=(0, 0, 0))
    scotomaLeft.draw()
    drawTags(screenAttributes)

    glClearColor(1, 1, 1, 1)
    glDrawBuffer(GL_BACK_RIGHT)
    glClear(GL_COLOR_BUFFER_BIT)
    scotomaLeft = shapes.Circle(x1+separation, y1, scotomaRadius, color=(0, 0, 0))
    scotomaLeft.draw()

    # display the april tags
    drawTags(screenAttributes)


# Launch the simulation screen ----------------------------------------------------------
def launchSimulation(screenAttributes, experimentAttributes):
    simulationWindow = createWindow(1)
    (screen_x, screen_y) = screenAttributes.get("ScreenSize")
    surfaceName = "surface"

    @simulationWindow.event
    def on_draw():
        (x, y) = getGazePosition(experimentAttributes.get("sub"), surfaceName)
        x = x * screen_x
        y = screen_y - y * screen_y
        drawAll(x, y, screenAttributes, experimentAttributes)

    pyglet.app.run()

