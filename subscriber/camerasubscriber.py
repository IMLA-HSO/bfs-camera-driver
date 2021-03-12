""" Subsribe to camera publisher. Received images are displayed.
python3 subscriber/camerasubscriber.py
"""

import argparse
import os
from typing import Dict, Tuple

import cv2
import numpy as np
import zmq


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


def get_arguments() -> Tuple[str, str, bool, str]:
    """Gets the arguments needed to run the subscriber.
    Returns:

    """
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--port_image",
        help="Port for subscribe image msg.",
        default=5557,
        type=int,
    )
    ap.add_argument(
        "--port_metadata",
        help="Port for subscribe image metadata.",
        default=5556,
        type=int,
    )

    ap.add_argument(
        "--address_image",
        help="Address for subscribe image msg.",
        default="tcp://localhost:",
        type=str,
    )

    ap.add_argument(
        "--address_metadata",
        help="Address for subscribe image metadata.",
        default="tcp://localhost:",
        type=str,
    )
    ap.add_argument(
        "--save_img",
        help="Save recived images as file",
        default=False,
        type=bool,
    )

    ap.add_argument(
        "--save_dir",
        help="Directory to save images only used if save_img=True",
        default="./data/img",
        type=str,
    )

    args: Dict = vars(ap.parse_args())
    port_image: int = args["port_image"]
    port_json: int = args["port_metadata"]
    addr_image: str = args["address_image"]
    addr_json: str = args["address_metadata"]
    save_img: bool = args["save_img"]
    save_dir: str = args["save_dir"]

    return addr_image + str(port_image), addr_json + str(port_json), save_img, save_dir


def main():
    full_addr_image, full_addr_json, save_img, save_dir = get_arguments()

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
        cv2.imshow("Frame:", rgb_img)
        if save_img:
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            cv2.imwrite(f"{save_dir}/{frame_id}.png", rgb_img)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break


if __name__ == "__main__":
    main()
