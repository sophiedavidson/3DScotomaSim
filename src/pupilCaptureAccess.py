"""
pupilCaptureAccess.py
Author: Sophie Davidson
Date: 2023

This module defines all connections made to pupil capture, including the initial connection and subscription to
a topic, but also the collecting of gaze data.

"""

# pupilCaptureAccess.py
# Sophie Davidson, 2022  for IMT Atlantique

# Imports --------------------------------------------------------------------------------------------
import zmq
from msgpack import loads


# Connect to the pupil capture application using the details provided by the user.
def launchConnection(connectionDetails):
    context = zmq.Context()

    # open a req port to talk to pupil
    addr = connectionDetails[0]  #   # remote ip or localhost
    req_port = connectionDetails[1]   # # same as in the pupil remote gui
    req = context.socket(zmq.REQ)
    req.connect("tcp://{}:{}".format(addr, req_port))
    # ask for the sub port
    req.send_string("SUB_PORT")
    sub_port = req.recv_string()

    # open a sub port to listen to pupil
    sub = context.socket(zmq.SUB)
    sub.connect("tcp://{}:{}".format(addr, sub_port))
    sub.setsockopt_string(zmq.SUBSCRIBE, "surface")

    return sub


# Get the current gaze position, and return these values.
def getGazePosition(sub, surfaceName):
    norm_gp_x = 0
    norm_gp_y = 0

    try:
        topic = sub.recv_string()
        msg = sub.recv()  # bytes
        surfaces = loads(msg, raw=False)
        filtered_surface = {
            k: v for k, v in surfaces.items() if surfaces["name"] == surfaceName
        }
        try:
            gaze_positions = filtered_surface["gaze_on_surfaces"]
            for gaze_pos in gaze_positions:
                norm_gp_x, norm_gp_y = gaze_pos["norm_pos"]

        except:
            pass
    except:
        pass

    return norm_gp_x, norm_gp_y

