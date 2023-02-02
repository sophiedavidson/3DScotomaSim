"""
file: simulation3D.py
name: Sophie Davidson
company:IMT Atlantique
date: 1/2023

    This module will generate a 3D stereoscopic window and display the simulated scotoma using data received from
    the eyetracker. April tags are used to configure the surface as defined in the Pupil Capture application.
    The scotoma can be adjusted using the control panel which is launched as a seperate window.

"""

# Imports
import pyglet
import tkinter as tk
from pyglet.gl import *
from pyglet import shapes
from threading import Thread

from controlPanel import ControlPanel
from pupilCaptureAccess import getGazePosition
from windowManagement import createWindow
from dataManagement import transformEyeData

# Globals
global x, y, surfaceCalibrated
global control_panel, left_location_slider, left_opacity_slider, left_size_slider, left_hide_checkbox_var
global right_location_slider, right_opacity_slider, right_size_slider, right_hide_checkbox_var


def runControlWindow():
    controlRoot = tk.Tk()
    control_panel = ControlPanel(controlRoot)
    controlRoot.mainloop()


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
    background.draw()
    (adjustedX, adjustedY) = transformEyeData(currentX, currentY, experimentAttributes.get("location"))
    scotomaLeft = shapes.Circle(adjustedX, adjustedY, scotomaRadius, color=(0, 0, 0))
    scotomaLeft.draw()
    #drawTags(screenAttributes)

    # Right Eye
    glClearColor(1, 1, 1, 1)
    glDrawBuffer(GL_BACK_RIGHT)
    glClear(GL_COLOR_BUFFER_BIT)
    background.draw()
    #drawTags(screenAttributes)
    scotomaRight = shapes.Circle(adjustedX + separation, adjustedY, scotomaRadius, color=(0, 0, 0))
    scotomaRight.draw()


# Set the surface calibrated variable to true after waiting for some time. This is time to allow the eye-tracker to
# detect the april tags and surface.
def setSurfaceCalibrated(dt):
    global surfaceCalibrated
    surfaceCalibrated = True
    print("done")
    return dt


# Launch the simulation screen ----------------------------------------------------------------------------------------
def launchSimulation(screenAttributes, experimentAttributes):

    global surfaceCalibrated
    surfaceCalibrated = False
    simulationWindow = createWindow(1)
    simulationWindow.set_mouse_visible(False)  # Hide the mouse cursor
    (screen_x, screen_y) = screenAttributes.get("ScreenSize")
    surfaceName = "surface"
    thread = Thread(target=runControlWindow)
    thread.start()

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

    # wait 5 seconds to begin simulation, this allows time for Pupil Capture to detect the surface.
    pyglet.clock.schedule_once(setSurfaceCalibrated, 5)

    pyglet.app.run()




