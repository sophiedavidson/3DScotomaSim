import threading
from threading import Thread
from tkinter import *
import pyglet
from controlPanel import ControlPanel

global get_left_opacity


def run_tkinter():
    global get_left_opacity
    controlRoot = Tk()
    control_panel = ControlPanel(controlRoot)
    controlRoot.mainloop()

    def get_left_opacity():
        return control_panel.left_opacity_slider.get()


def run_pyglet():
    window = pyglet.window.Window(caption="Pyglet")
    pyglet.app.run()

    @window.event
    def on_draw():
        print(get_left_opacity())





t1 = Thread(target=run_pyglet)
t2 = Thread(target=run_tkinter)

t1.start()
t2.start()


