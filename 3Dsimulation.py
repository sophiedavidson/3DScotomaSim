# Sophie Davidson 2022, for IMT Atlantique

# Imports
import pyglet
from pyglet.gl import *
import tkinter
from tkinter import messagebox


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


def get_screens():
    # Checking Available Screens
    display = pyglet.canvas.get_display()
    currentScreen = display.get_screens()
    return currentScreen


def displayError(message):
    master = tkinter.Tk()
    master.withdraw()
    messagebox.showerror(title="Configuration", message=message)


def createWindow(isStereo, screen):
    screens = get_screens()
    config = Config()
    config.stereo = isStereo
    config.fullscreen = True
    config.double_buffer = True
    newWindow = False
    try:
        newWindow = pyglet.window.Window(screen=screens[screen], config=config)
    except pyglet.window.NoSuchConfigException:
        displayError("No 3D display found:\nEnsure the device is compatible, and 3D mode is active")
        quit()
    except IndexError:
        displayError("No Secondary Display Detected")
        quit()
    return newWindow


def getTags(win):
    FULL_SIZE_TAG = 226
    scale = 0.5
    buffer = FULL_SIZE_TAG*scale
    tag1Img = pyglet.resource.image("media/tag1.jpg")
    tag1 = pyglet.sprite.Sprite(tag1Img, 0, win.height - buffer)
    tag2Img = pyglet.resource.image("media/tag2.jpg")
    tag2 = pyglet.sprite.Sprite(tag2Img, 0, 0)
    tag3Img = pyglet.resource.image("media/tag3.jpg")
    tag3 = pyglet.sprite.Sprite(tag3Img, win.width-buffer, win.height-buffer)
    tag4Img = pyglet.resource.image("media/tag4.jpg")
    tag4 = pyglet.sprite.Sprite(tag4Img, win.width-buffer, 0)
    tags = {"tag1": tag1, "tag2": tag2, "tag3": tag3, "tag4": tag4}
    for tag in tags.values(): tag.scale = scale
    return tags


def getBackground():
    backgroundImg = pyglet.resource.image("media/background.jpg")
    background = pyglet.sprite.Sprite(backgroundImg, 0,0)
    return background


def drawBasis(win):
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    tags = getTags(win)
    getBackground().draw()
    tags.get("tag1").draw()
    tags.get("tag2").draw()
    tags.get("tag3").draw()
    tags.get("tag4").draw()


def drawLeftView(win):
    glClearColor(1, 1, 1, 1)  # white
    glDrawBuffer(GL_BACK_LEFT)
    glClear(GL_COLOR_BUFFER_BIT)
    drawBasis(win)


def drawRightView(win):
    glClearColor(1, 1, 1, 1)  # white
    glDrawBuffer(GL_BACK_RIGHT)
    glClear(GL_COLOR_BUFFER_BIT)
    drawBasis(win)


def main():
    simulationWindow = createWindow(True, 1)
    controlWindow = createWindow(False, 0)

    @simulationWindow.event
    def on_draw():
        drawLeftView(simulationWindow)
        drawRightView()

    pyglet.app.run()


if __name__ == "__main__":
    main()


