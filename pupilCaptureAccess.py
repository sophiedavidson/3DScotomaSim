# pupilCaptureAccess.py
# Sophie Davidson, 2022  for IMT Atlantique

# Imports --------------------------------------------------------------------------------------------
import zmq
import socket
from msgpack import loads


def getIP():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    return IPAddr


def launchConnection(experimentAttributes):
    context = zmq.Context()

    if experimentAttributes.get("tracker") == "Pupil Labs Core Remote":
        ipTcpDetails = experimentAttributes.get("remoteDetails")
        addr = ipTcpDetails[0]
        req_port = ipTcpDetails[1]
    else:
        addr = "127.0.0.1"
        req_port = "50020"  # same as in the pupil remote gui
    req = context.socket(zmq.REQ)
    req.connect("tcp://{}:{}".format(addr, req_port))
    # ask for the sub port
    req.send_string("SUB_PORT")
    print("Attempting Connection....")
    sub_port = req.recv_string()
    print("Connection Successful")

    # open a sub port to listen to pupil
    sub = context.socket(zmq.SUB)
    sub.connect("tcp://{}:{}".format(addr, sub_port))
    sub.setsockopt_string(zmq.SUBSCRIBE, "surface")

    return sub


def getGazePosition(sub, surfaceName):
    norm_gp_x = 0
    norm_gp_y = 0

    try:
        topic = sub.recv_string()
        print(topic)
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
            print("getting gaze positions on surface failed")
    except:
        print("getting surface not possible")

    return norm_gp_x, norm_gp_y
