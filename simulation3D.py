# simulation.py
# Sophie Davidson for IMT Atlantique, 2022

# The following module generates the main screen of the program, including
# the April Tag Markers to be used for configuration of the device, and the
# simulated scotoma over a text background.

# Imports
from threading import Thread
import pyglet
import tkinter as tk
import time
from tkinter import messagebox
from pyglet.gl import *
from pyglet.window import NoSuchConfigException
from pyglet import shapes
from pupilCaptureAccess import getGazePosition
from controlWindow import ControlPanel
global x,y, surfaceCalibrated
x=50
y=50
surfaceCalibrated = False


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
    background.scale = 0.5
    scotomaRadius = experimentAttributes.get("radius")
    separation = experimentAttributes.get("separation")

    # Left Eye
    glClearColor(1, 1, 1, 1)
    glDrawBuffer(GL_BACK_LEFT)
    glClear(GL_COLOR_BUFFER_BIT)
    (x1, y1) = transformEyeData(x, y, experimentAttributes.get("location"))
    scotomaLeft = shapes.Circle(x1, y1, 20, color=(0, 0, 0))
    scotomaLeft.draw()
    drawTags(screenAttributes)


    # Right Eye
    glClearColor(1, 1, 1, 1)
    glDrawBuffer(GL_BACK_RIGHT)
    glClear(GL_COLOR_BUFFER_BIT)
    drawTags(screenAttributes)
    scotomaRight = shapes.Circle(x1+separation, y1, scotomaRadius, color=(0, 0, 0))
    scotomaRight.draw()

def setSurfaceCalibrated(dt):
    global surfaceCalibrated
    surfaceCalibrated = True
    print("done")


def runControlPanel():
    root = tk.Tk()
    controlPanel = ControlPanel(root)
    root.mainloop()
# Launch the simulation screen ----------------------------------------------------------


def launchSimulation(screenAttributes, experimentAttributes):
    global surfaceCalibrated
    simulationWindow = createWindow(1)
    simulationWindow.set_mouse_visible(False)
    (screen_x, screen_y) = screenAttributes.get("ScreenSize")
    surfaceName = "surface"
    t1 = Thread(target=runControlPanel)
    t1.start()



    @simulationWindow.event
    def on_draw():
        global surfaceCalibrated
        if surfaceCalibrated == False:
            x,y = 0,0
        if surfaceCalibrated == True:
            (x,y)=getGazePosition(experimentAttributes.get("sub"),"surface")
        x=x*screen_x
        y=y*screen_y
        drawAll(x, y, screenAttributes, experimentAttributes)
    """
    @simulationWindow.event
    def on_mouse_motion(thisX, thisY, dx, dy):
        global x, y
        x = thisX #* screen_x
        y = thisY   #screen_y - thisY * screen_y
    """
    pyglet.clock.schedule_once(setSurfaceCalibrated, 5)

    pyglet.app.run()

