"""
simulation3D.py
Author: Sophie Davidson
Date: 2023

This module generates the simulation screen, and on a seperate thread, the control panel.

"""
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
def drawAll(currentX, currentY, screenAttributes, experimentAttributes):
    # get details required
    global controlPanel

    # Scotoma details
    (xLeft, yLeft) = transformEyeData(currentX, currentY, 0)
    (xRight, yRight) = transformEyeData(currentX, currentY, 1)
    scotomaRadiusLeft = controlPanel.left_size_slider.get()
    scotomaRadiusRight = controlPanel.right_size_slider.get()
    separation = controlPanel.offset_slider.get()
    scotomaLeft = shapes.Circle(xLeft, yLeft, scotomaRadiusLeft, color=(0, 0, 0))
    scotomaRight = shapes.Circle(xRight+separation, yRight, scotomaRadiusRight, color=(0, 0, 0))

    #Stimulus details
    textStimulus = experimentAttributes.get("stimulus")
    textSize= controlPanel.font_size_slider.get()
    label = pyglet.text.Label(text=textStimulus,
                              color=(0,0,0,255),
                              font_size=textSize,
                              x=600,
                              y=400,
                              anchor_x="center")

    circleStim = shapes.Circle(300, 100, 40,color=(255,0,0,255))

    starStim1 = shapes.Star(600+separation,100,60,40,color = (0,255,0,255),num_spikes =5)
    starStim2 = shapes.Star(600,100,60,40,color = (0,255,0,255),num_spikes=5)

    squareStim1 = shapes.Rectangle(900, 100, 80,80, color=(0,0,255,255))
    squareStim2 = shapes.Rectangle(900+separation+10,100,80,80, color=(0,0,255,255))

    # Left Eye
    glClearColor(1, 1, 1, 1)
    glDrawBuffer(GL_BACK_LEFT)
    glClear(GL_COLOR_BUFFER_BIT)
    circleStim.draw()
    starStim1.draw()
    drawTags(screenAttributes)
    label.draw()
    scotomaLeft.draw()
    squareStim1.draw()


    # Right Eye
    glClearColor(1, 1, 1, 1)
    glDrawBuffer(GL_BACK_RIGHT)
    glClear(GL_COLOR_BUFFER_BIT)
    circleStim.draw()
    starStim2.draw()
    drawTags(screenAttributes)
    label.draw()
    scotomaRight.draw()
    squareStim2.draw()


# This function is called after the experiment screen has been opened for 5 seconds,
# once the tracker has had time to recognise the surface.
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
    # Start the control panel on a seperate thread.
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
        drawAll(x, y, screenAttributes, experimentAttributes)

    pyglet.clock.schedule_once(setSurfaceCalibrated, 5)

    pyglet.app.run()
