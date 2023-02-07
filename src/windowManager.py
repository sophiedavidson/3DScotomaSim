import pyglet
from dialogue import showMessage
from pyglet.window import NoSuchConfigException
from pyglet.gl import *


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