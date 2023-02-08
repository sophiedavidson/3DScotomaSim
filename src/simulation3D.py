# simulation.py
# Sophie Davidson for IMT Atlantique, 2022

# The following module generates the main screen of the program, including
# the April Tag Markers to be used for configuration of the device, and the
# simulated scotoma over a text background.

# Imports
import pyglet
import tkinter as tk
from pyglet.gl import *
from pyglet import shapes
from threading import Thread

# Module Imports
from pupilCaptureAccess import getGazePosition
from controlWindow import ControlPanel
from windowManager import createWindow

global surfaceCalibrated, controlPanel


# Moves the scotoma to a relative location.
def transformEyeData(transformX, transformY, eye):
    global controlPanel
    if eye == 0:
        locationString = controlPanel.left_location_slider.dot_location.get()
        locationString = locationString[1:-1].split(",")
        (xAdd, yAdd) = (int(locationString[0]), int(locationString[1]))
    else:
        locationString = controlPanel.right_location_slider.dot_location.get()
        locationString = locationString[1:-1].split(",")
        (xAdd, yAdd) = (int(locationString[0]), int(locationString[1]))

    transformX = transformX + xAdd
    transformY = transformY - yAdd
    return transformX, transformY


# Draws the april tags
def drawTags(screenAttributes):
    # get required attributes
    tags = screenAttributes.get("Tags")

    tags[0].draw()
    tags[1].draw()
    tags[2].draw()
    tags[3].draw()


# Draws all the foreground components
def drawAll(currentX, currentY, screenAttributes):
    # get details required
    global controlPanel

    (xLeft, yLeft) = transformEyeData(currentX, currentY, 0)
    (xRight, yRight) = transformEyeData(currentX, currentY, 1)

    scotomaRadiusLeft = controlPanel.left_size_slider.get()
    scotomaRadiusRight = controlPanel.right_size_slider.get()

    separation = controlPanel.offset_slider.get()

    scotomaLeft = shapes.Circle(xLeft, yLeft, scotomaRadiusLeft, color=(0, 0, 0))
    scotomaRight = shapes.Circle(xRight+separation, yRight, scotomaRadiusRight, color=(0, 0, 0))

    textSize= controlPanel.font_size_slider.get()
    label = pyglet.text.Label(text="Testing 123 Testing",
                              color=(0,0,0,255),
                              font_size=textSize,
                              x=600,
                              y=400,
                              anchor_x="center")

    # Left Eye
    glClearColor(1, 1, 1, 1)
    glDrawBuffer(GL_BACK_LEFT)
    glClear(GL_COLOR_BUFFER_BIT)
    drawTags(screenAttributes)
    label.draw()
    scotomaLeft.draw()

    # Right Eye
    glClearColor(1, 1, 1, 1)
    glDrawBuffer(GL_BACK_RIGHT)
    glClear(GL_COLOR_BUFFER_BIT)
    drawTags(screenAttributes)
    label.draw()
    scotomaRight.draw()


def setSurfaceCalibrated(dt):
    global surfaceCalibrated
    surfaceCalibrated = True
    print(dt)


def runControlPanel():
    global controlPanel
    root = tk.Tk()
    controlPanel = ControlPanel(root)
    root.mainloop()
# Launch the simulation screen ----------------------------------------------------------


def launchSimulation(screenAttributes, experimentAttributes):
    global surfaceCalibrated
    surfaceCalibrated = False
    t1 = Thread(target=runControlPanel)
    t1.start()
    simulationWindow = createWindow(1)
    simulationWindow.set_mouse_visible(False)
    (screen_x, screen_y) = screenAttributes.get("ScreenSize")

    @simulationWindow.event
    def on_draw():
        global surfaceCalibrated
        if surfaceCalibrated:
            (x, y) = getGazePosition(experimentAttributes.get("sub"), "surface")
        else:
            (x, y) = (50, 50)

        x = x*screen_x
        y = y*screen_y
        drawAll(x, y, screenAttributes)

    pyglet.clock.schedule_once(setSurfaceCalibrated, 5)

    pyglet.app.run()
