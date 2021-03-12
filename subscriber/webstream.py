""" Subsribe to camera publisher. Received images are displayed to 'web'.
python3 subscriber/webstream.py
"""

from flask import Flask, render_template, Response
import cv2
import numpy as np
import zmq

app = Flask(__name__)


def recv_image(socket_img, socket_json, flags=0, copy=False, track=False):
    """recv a numpy array"""

    msg = socket_json.recv_json(flags=flags)
    img_msg = socket_img.recv(flags=flags, copy=copy, track=track)
    buf = memoryview(img_msg)
    img = np.frombuffer(buf, dtype=msg["dtype"])
    return (
        img.reshape(msg["shape"]),
        msg["timestamp"],
        msg["frame_id"],
    )


def get_image():
    full_addr_image = "tcp://localhost:5557"
    full_addr_json = "tcp://localhost:5556"

    context = zmq.Context()
    cam_socket_img = context.socket(zmq.SUB)
    cam_socket_img.setsockopt_string(zmq.SUBSCRIBE, "")
    cam_socket_img.setsockopt(zmq.CONFLATE, 1)
    cam_socket_img.connect(full_addr_image)

    cam_socket_json = context.socket(zmq.SUB)
    cam_socket_json.setsockopt_string(zmq.SUBSCRIBE, "")
    cam_socket_json.setsockopt(zmq.CONFLATE, 1)
    cam_socket_json.connect(full_addr_json)

    print("Start recive")
    while True:
        img, timestamp, frame_id = recv_image(cam_socket_img, cam_socket_json)
        rgb_img = img[..., ::-1]
        ret, buffer = cv2.imencode(".jpg", rgb_img)
        frame = buffer.tobytes()
        yield (
            b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        )  # concat frame one by one and show result


@app.route("/zumi-cam")
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(get_image(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/")
def index():
    """Video streaming home page."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
