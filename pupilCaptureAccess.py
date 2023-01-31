"""
file: pupilCaptureAccess.py
name: Sophie Davidson
company:IMT Atlantique
date: 1/2023

    This module defines all the methods required for communication with Pupil Capture software, including the collection
    process and the gathering of gaze data.
"""

# Imports --------------------------------------------------------------------------------------------
import zmq
from msgpack import loads


# Tries to connect to the pupil capture application using the address and port information supplied by the user.
def launchConnection(experimentAttributes):
    context = zmq.Context()

    # if the tracker is remote, get the details entered by the user.
    print(experimentAttributes.get("tracker"))
    if experimentAttributes.get("tracker") == "Pupil Labs Core Remote":
        ipTcpDetails = experimentAttributes.get("remoteDetails")
        addr = ipTcpDetails[0]
        req_port = ipTcpDetails[1]
    # if local, use the localhost address and default ports.
    else:
        addr = "127.0.0.1"
        req_port = "50020"  # same as in the pupil remote gui
    # connect using the defined address and port
    req = context.socket(zmq.REQ)
    req.connect("tcp://{}:{}".format(addr, req_port))
    # ask for the sub port
    req.send_string("SUB_PORT")
    print("Attempting Connection....")
    sub_port = req.recv_string()
    print("Connection Successful")

    # open a sub port to listen to gaze on surface information.
    sub = context.socket(zmq.SUB)
    sub.connect("tcp://{}:{}".format(addr, sub_port))
    sub.setsockopt_string(zmq.SUBSCRIBE, "surface")

    # return the subscription data so that the connection can be used later
    return sub


# Get the current gaze position on the defined surface.
def getGazePosition(sub, surfaceName):
    norm_gp_x = 0
    norm_gp_y = 0

    try:
        # try to communicate with Pupil.
        topic = sub.recv_string()
        msg = sub.recv()  # bytes
        surfaces = loads(msg, raw=False)
        # accept the filtered gaze data from pupil
        filtered_surface = {
            k: v for k, v in surfaces.items() if surfaces["name"] == surfaceName
        }
        try:
            gaze_positions = filtered_surface["gaze_on_surfaces"]
            for gaze_pos in gaze_positions:
                norm_gp_x, norm_gp_y = gaze_pos["norm_pos"]
        # TODO - Make the except statements more precise/useful.
        except:
            print("getting gaze positions on surface failed")
    except:
        print("getting surface not possible")

    # return the normalised x and y positions.
    return norm_gp_x, norm_gp_y
