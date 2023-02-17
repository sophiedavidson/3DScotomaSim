# Asymmetric Scotoma Simulation (3DScotomaSim)
Adjustable asymmetric scotoma created using 3D active glasses and the Pupil Core eyetracker.
 
 ## About the Project
 
 **Author**: Sophie Davidson     
 **Purpose**:  Generate a simulated asymmetric scotoma.
 
 **Context**: This project was completed as part of the Nicholas Baudin internships in France program. Thank you for the support of my host institution, IMT Atlantique, and Orthoptica.
 
**Dependencies:** 
- pyglet
- msgpack 
- zmq
- os
 

## To Open Application (Non Developer) 

Download the .exe application file then double click to open the application (dist/Asymmetric Scotoma Simulator.exe)

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

## .exe File Generation
To create a new .exe, first install pyinstaller using 

```
py -m pip install pyinstaller
```
then cd into the source directory, you may need to move all images in media to the src folder, and change the references to these images in driver.py. 
In dialogue.py you may also need to change exit() into sys.quit()
Finally, run the following script in the terminal.

```
py -m PyInstaller driver.py --onefile --windo
wed --add-data "tag1.jpg;." --add-data "tag2.jpg;." --add-data "tag3.jpg;." --add-data "ta
g4.jpg;." --hidden-import "pyglet" --hidden-import "zmq" --hidden-import "msgpck"
```

