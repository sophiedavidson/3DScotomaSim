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

# Module Imports
from pupilCaptureAccess import getGazePosition

# Globals
global x, y, surfaceCalibrated


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
        # note that if isStereoscopic, tries to display on secondary screen ([1])
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
def transformEyeData(thisX, thisY, location):
    if location == "N":
        thisY = thisY - 50
    elif location == "NE":
        thisX = thisX + 50
        thisY = thisY - 50
    elif location == "E":
        thisX = thisX + 50
    elif location == "SE":
        thisX = thisX + 50
        thisY = thisY + 50
    elif location == "S":
        thisY = thisY + 50
    elif location == "SW":
        thisX = thisX - 50
        thisY = thisY + 50
    elif location == "W":
        thisX = thisX - 50
    elif location == "NW":
        thisX = thisX - 50
        thisY = thisY - 50
    return thisX, thisY


# Draws the april tags
def drawTags(screenAttributes):
    # get required attributes
    tags = screenAttributes.get("Tags")

    tags[0].draw()
    tags[1].draw()
    tags[2].draw()
    tags[3].draw()


# Draws all of the foreground components
def drawAll(currentX, currentY, screenAttributes, experimentAttributes):
    background = screenAttributes.get("Background")
    background.scale = 0.5
    scotomaRadius = experimentAttributes.get("radius")
    separation = experimentAttributes.get("separation")

    # Left Eye
    glClearColor(1, 1, 1, 1)
    glDrawBuffer(GL_BACK_LEFT)
    glClear(GL_COLOR_BUFFER_BIT)
    (adjustedX, adjustedY) = transformEyeData(currentX, currentY, experimentAttributes.get("location"))
    scotomaLeft = shapes.Circle(adjustedX, adjustedY, scotomaRadius, color=(0, 0, 0))
    scotomaLeft.draw()
    drawTags(screenAttributes)

    # Right Eye
    glClearColor(1, 1, 1, 1)
    glDrawBuffer(GL_BACK_RIGHT)
    glClear(GL_COLOR_BUFFER_BIT)
    drawTags(screenAttributes)
    scotomaRight = shapes.Circle(adjustedX + separation, adjustedY, scotomaRadius, color=(0, 0, 0))
    scotomaRight.draw()


def setSurfaceCalibrated(dt):
    global surfaceCalibrated
    surfaceCalibrated = True
    print("done")
    return dt


# Launch the simulation screen ----------------------------------------------------------
def launchSimulation(screenAttributes, experimentAttributes):
    global surfaceCalibrated
    surfaceCalibrated = False
    simulationWindow = createWindow(1)
    simulationWindow.set_mouse_visible(False)
    (screen_x, screen_y) = screenAttributes.get("ScreenSize")
    surfaceName = "surface"

    @simulationWindow.event
    def on_draw():
        (x, y) = (0, 0)
        if experimentAttributes.get("Tracker") == "Mouse":
            @simulationWindow.event
            def on_mouse_motion(thisX, thisY, dx, dy):
                global x, y
                x = thisX  # * screen_x
                y = thisY   # screen_y - thisY * screen_y
                return dx, dy
        else:
            global surfaceCalibrated
            if not surfaceCalibrated:
                pass
            else:
                (x, y) = getGazePosition(experimentAttributes.get("sub"), surfaceName)
            x = x*screen_x
            y = y*screen_y

        drawAll(x, y, screenAttributes, experimentAttributes)

    # TODO - Wait until first correct data point is received to start main loop rather than just waiting 5sec.
    # TODO - Fix error where freezes when no data is received (ie - check if none case)
    pyglet.clock.schedule_once(setSurfaceCalibrated, 5)

    pyglet.app.run()
