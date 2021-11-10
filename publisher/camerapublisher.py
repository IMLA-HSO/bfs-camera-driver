""" CameraPublisher: Publish images from BFS-Camera.
"""

import argparse
import time
from time import sleep
from typing import Dict, Tuple
 
####################
import numpy as np

import cv2 as cv

import glob

####################

import PySpin
import zmq

####################
import yaml


class ImagePublisher(object):
    def __init__(self, addr_image="tcp://0.0.0.0:5557", addr_json="tcp://0.0.0.0:5556"):
        context = zmq.Context()
        self.json_socket = context.socket(zmq.PUB)
        self.json_socket.bind(addr_json)

        self.img_socket = context.socket(zmq.PUB)
        self.img_socket.bind(addr_image)

    def send_data(self, image, timestamp, frame_id, flags=0, copy=True, track=False):
        msg = dict(
            dtype=str(image.dtype),
            shape=image.shape,
            timestamp=timestamp,
            frame_id=frame_id,
        )
        self.json_socket.send_json(msg, flags)
        self.img_socket.send(image, flags, copy=copy, track=track)


class CameraBFS(object):
    def __init__(self, cam: PySpin.Camera, image_publisher: ImagePublisher):
        self.image_publisher = image_publisher
        self.cam = cam
        self.cam.Init()
        self.cam.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)
        self.cam.TLStream.StreamBufferHandlingMode.SetValue(
            PySpin.StreamBufferHandlingMode_NewestOnly
        )

        self.nodemap = cam.GetNodeMap()
        self.configure_chunk_data(self.nodemap)

    def configure_chunk_data(self, nodemap):
        try:
            print("\n*** CONFIGURING CHUNK DATA ***\n")
            chunk_mode_active = PySpin.CBooleanPtr(nodemap.GetNode("ChunkModeActive"))

            if PySpin.IsAvailable(chunk_mode_active) and PySpin.IsWritable(
                chunk_mode_active
            ):
                chunk_mode_active.SetValue(True)

            print("Chunk mode activated...")
            chunk_selector = PySpin.CEnumerationPtr(nodemap.GetNode("ChunkSelector"))

            if not PySpin.IsAvailable(chunk_selector) or not PySpin.IsReadable(
                chunk_selector
            ):
                print("Unable to retrieve chunk selector. Aborting...\n")
                return False

            entries = [
                PySpin.CEnumEntryPtr(chunk_selector_entry)
                for chunk_selector_entry in chunk_selector.GetEntries()
            ]

            print("Enabling entries...")

            for chunk_selector_entry in entries:
                if not PySpin.IsAvailable(
                    chunk_selector_entry
                ) or not PySpin.IsReadable(chunk_selector_entry):
                    continue

                chunk_selector.SetIntValue(chunk_selector_entry.GetValue())

                chunk_str = "\t {}:".format(chunk_selector_entry.GetSymbolic())

                chunk_enable = PySpin.CBooleanPtr(nodemap.GetNode("ChunkEnable"))

                if not PySpin.IsAvailable(chunk_enable):
                    print("{} not available".format(chunk_str))
                elif chunk_enable.GetValue() is True:
                    print("{} enabled".format(chunk_str))
                elif PySpin.IsWritable(chunk_enable):
                    chunk_enable.SetValue(True)
                    print("{} enabled".format(chunk_str))
                else:
                    print("{} not writable".format(chunk_str))

        except PySpin.SpinnakerException as ex:
            print("Error: %s" % ex)

    def stop(self):
        self.cam.DeInit()

    def run(self, fps=60):
        try:
            self.cam.BeginAcquisition()
            print("Acquiring images...")

            waittime = 1000 / int(fps)

            while True:
                now = time.time()

                image_result = self.cam.GetNextImage(1000)

                if image_result.IsIncomplete():
                    print(
                        "Image incomplete with image status %d ..."
                        % image_result.GetImageStatus()
                    )

                else:
                    rgb_image = image_result.Convert(
                        PySpin.PixelFormat_RGB8, PySpin.HQ_LINEAR
                    )
                    chunk_data = image_result.GetChunkData()
                    rgb_image = rgb_image.GetData()
                    height = chunk_data.GetHeight()
                    width = chunk_data.GetWidth()
                    # Timestamp does not work properly on Linux systems. Known spinnaker bug (30.11.2020)
                    timestamp = chunk_data.GetTimestamp()
                    frame_id = chunk_data.GetFrameID()

                    rgb_image = rgb_image.reshape([height, width, 3])
                    
                    ##################################  CALIBRATITION  #########################################
                    with open('calibration.yaml') as fh:
                        read_data = yaml.load(fh, Loader = yaml.FullLoader)
                        matx = read_data['camera_matrix']
                        dist_coeff = read_data['dist_coeff']

                        matx = np.array(matx)
                        dist_coeff = np.array(dist_coeff)
                                 
                    newcameramtx, roi = cv.getOptimalNewCameraMatrix(matx, dist_coeff, (width,height), 1, (width,height))
                    dst = cv.undistort(rgb_image, matx, dist_coeff, None, newcameramtx)
                    x, y, w, h = roi
                    dst = dst[y:y+h, x:x+w]

                    self.image_publisher.send_data(dst.astype('uint8'), timestamp, frame_id)

                image_result.Release()

                diff = time.time() - now
                beat = waittime - diff
                sleep(beat / 1000.0)

        except PySpin.SpinnakerException as ex:
            print("Error: %s" % ex)
        except KeyboardInterrupt:
            pass
        finally:
            self.cam.EndAcquisition()


def get_arguments() -> Tuple[int, str, str]:
    """Gets the arguments needed to run the publisher.
    Returns:

    """
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--port_image",
        help="Port for publish image msg.",
        default=5557,
        type=int,
    )
    ap.add_argument(
        "--port_metadata",
        help="Port for publish image metadata.",
        default=5556,
        type=int,
    )

    ap.add_argument(
        "--address_image",
        help="Address for publish image msg.",
        default="tcp://0.0.0.0:",
        type=str,
    )

    ap.add_argument(
        "--address_metadata",
        help="Address for publish image metadata.",
        default="tcp://0.0.0.0:",
        type=str,
    )

    ap.add_argument(
        "-f",
        "--fps",
        help="Address for subscribe image metadata.",
        default=30,
        type=int,
    )

    args: Dict = vars(ap.parse_args())
    port_image: int = args["port_image"]
    port_json: int = args["port_metadata"]
    addr_image: str = args["address_image"]
    addr_json: str = args["address_metadata"]
    fps: int = args["fps"]
    return fps, addr_image + str(port_image), addr_json + str(port_json)


def main():
    fps, full_addr_image, full_addr_json = get_arguments()

    # Retrieve singleton reference to system object
    system = PySpin.System.GetInstance()

    version = system.GetLibraryVersion()
    print(
        "PySpin library version: %d.%d.%d.%d"
        % (version.major, version.minor, version.type, version.build)
    )

    cam_list = system.GetCameras()
    if not cam_list.GetSize():
        print("No cameras detected")
        return

    image_publisher = ImagePublisher(full_addr_image, full_addr_json)
    camera = CameraBFS(cam_list[0], image_publisher)

    try:
        camera.run(fps)
    except KeyboardInterrupt:
        pass
    finally:
        camera.stop()
        del camera
        cam_list.Clear()
        system.ReleaseInstance()


if __name__ == "__main__":
    main()
