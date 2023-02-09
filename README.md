# Asymmetric Scotoma Simulation (3DScotomaSim)
Adjustable asymmetric scotoma created using 3D active glasses and the Pupil Core eyetracker.
 
 ## About the Project
 
 **Author**: Sophie Davidson     
 **Purpose**:  Generate a simulated asymmetric scotoma.
 
**Dependencies:** 
- pyglet
- msgpack 
- zmq
- os
 

## To Open Application (Non Developer) 

Download the .exe application file then double click to open the application. 

Note that you may need to "Trust" the file first once it has been downloaded. 

Please see the guide, which can be found within the docs folder. 

**Requirements:**

Either:
A windows 10 or higher system with a NVIDIA Quatro, or other stereoscopic capable graphics card with the pupil capture application installed.
A 3D capable projector and active shutter glasses.

Or  

One windows 10 or higher system with the pupil capture application installed, and a separate machine with a stereoscopic capable graphics card. This option also requires either an ethernet or network connection. 
A 3D capable projector and active shutter glasses.
        
## How to Install Dependencies


```
py -m pip install pyglet, msgpack, zmq, os
```

To check that the packages have installed, use 
``` 
py -m pip freeze
```
