"""
file: controlPanel.py
name: Sophie Davidson
company:IMT Atlantique
date: 1/2023

 The following class defines the functionality of the Control Panel used to adjust the characteristics of the
 3D scotoma simulation

"""

# Imports
import tkinter as tk

"""
LocationSelector Class: Defines a 2D region containing a dot which can be moved. The dot represents the scotoma's 
relative location in the field of vision. 
"""


class LocationSelector:
    def __init__(self, root, sync_var=None):
        # generating the sub-screen to be displayed.
        self.root = root
        self.canvas = tk.Canvas(root, width=200, height=200, background="white")
        self.canvas.pack()

        # generating the dot, and defining its characteristics
        self.dot = self.canvas.create_oval(90, 90, 110, 110, fill="red")
        self.canvas.bind("<B1-Motion>", self.update_location)  # if the dot is moved, call the update_location method
        # when the dot is moved, update the dot_location variable
        self.dot_location = tk.StringVar()
        self.dot_location_label = tk.Label(root, textvariable=self.dot_location)
        self.dot_location_label.pack()
        self.dot_location.set("(0, 0)")  # Initial position
        self.sync_var = sync_var

    # define what to do when the dot is moved.
    def update_location(self, event):
        x, y = event.x, event.y
        self.canvas.coords(self.dot, x - 10, y - 10, x + 10, y + 10)
        self.dot_location.set(f"({x - 100}, {y - 100})")  # Update the position
        if self.sync_var and self.sync_var.get() == 1:
            self.root.event_generate("<SyncEvent>", x=x, y=y)



"""
ControlPanel Class: Defines a control panel window containing controls for size,relative location and visibility of the
scotoma simulated for each eye as well as the offset between the two eyes (ie the apparent z distance of the scotoma).
"""


class ControlPanel:
    def __init__(self, root):
        self.root = root
        root.title("Control Panel")

        # left side controls
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side="left")
        self.left_label = tk.Label(self.left_frame, text="Left")
        self.left_label.pack()
        # 2D location selector (left)
        self.left_location_slider = LocationSelector(self.left_frame)

        # Size slider (left)
        self.left_size_slider = tk.Scale(self.left_frame, from_=0, to=200, orient="horizontal", label="Size")
        self.left_size_slider.pack()
        # Determines whether the left side scotoma should be hidden or shown.
        self.left_hide_checkbox_var = tk.IntVar()
        self.left_hide_checkbox = tk.Checkbutton(self.left_frame, text="Hide", variable=self.left_hide_checkbox_var)
        self.left_hide_checkbox.pack()

        # Right side controls
        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side="right")
        self.right_label = tk.Label(self.right_frame, text="Right")
        self.right_label.pack()
        # 2D location selector (right)
        self.right_location_slider = LocationSelector(self.right_frame)

        # Size slider (right)
        self.right_size_slider = tk.Scale(self.right_frame, from_=0, to=200, orient="horizontal", label="Size")
        self.right_size_slider.pack()
        # Determines whether the right side scotoma should be hidden or shown
        self.right_hide_checkbox_var = tk.IntVar()
        self.right_hide_checkbox = tk.Checkbutton(self.right_frame, text="Hide", variable=self.right_hide_checkbox_var)
        self.right_hide_checkbox.pack()

        # Central controls
        self.offset_slider = tk.Scale(from_=-100, to=100, orient="horizontal", label="Left/Right Offset")
        self.offset_slider.pack()
        # TODO - Sync checkbox doesn't work
        # self.sync_checkbox_var = tk.IntVar()
        # self.sync_checkbox = tk.Checkbutton(root, text="Synchronize", variable=self.sync_checkbox_var)
        # self.sync_checkbox.pack()



if __name__ == "__main__":
    root = tk.Tk()
    controlPanel = ControlPanel(root)
    root.mainloop()
