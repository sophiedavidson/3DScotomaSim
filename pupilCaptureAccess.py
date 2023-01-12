# pupilCaptureAccess.py
# Sophie Davidson, 2022  for IMT Atlantique

# Imports --------------------------------------------------------------------------------------------
import zmq
from msgpack import loads


def launchConnection():
    context = zmq.Context()
    # open a req port to talk to pupil
    addr = "127.0.0.1"  # remote ip or localhost
    req_port = "50020"  # same as in the pupil remote gui
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

