# 3DScotomaSim

 <h2>About the Project </h2>
 
**Author:** Sophie Davidson 

**Topic:** Made for IMT Atlantique as part of the Baudin Internships in France Program

**Purpose:** Generate a simulated scotoma using Pupil Labs eye tracking technology and a 3D projector

**Dependencies**: pyglet, tkinter, os, zmq, msgpack

 <h2>How to Install Dependencies </h2>
 
 Uing Windows Powershell, type:
 
  ```
  py -m pip install pyglet, tkinter, os, zmq, msgpack, socket
  ```

 
 To check that the packages have installed, use
 
 ``` 
 py -m pip freeze
 ```
 

**Pupil Capture Software**: Must be installed, to begin an experiment, open the pupil capture software and define a surface by opening the sample test image. The surface must be named "surface". 

Ensure that the Network API and Surface Tracking plugins are selected, and that both eyes are selected in the general settings pane. 


**3D Settings**
In order for the 3D functionality to work as expected please ensure the following settings:
1280x800, True Colour (32 bit), 120Hz. 
In NVIDIA  Control Panel, reset 3D settings to default, then ensure that Stereo-enable is On, Swap-mode is set to "application controlled, and Stereo-Swap-Eyes is Off. 

Note: If using remote access, ensure firewalls are turned off as this can block the incoming/outgoing signals

