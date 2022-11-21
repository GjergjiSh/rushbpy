import cv2
import logging
from rushb.modules.RBModule import *


class VideoCapture(RBModule):
    """VideoCapture is a class that captures the video feed from the webcam
     and writes it to the shared memory"""

    def __init__(self, **kwargs) -> None:
        self.video_capture = None
        self.camera_id = kwargs.get("camera_id")

    def init(self) -> None:
        # Initialize the video capture
        logging.info("Initializing VideoCapture")

        # Check if the camera id is not None
        if self.camera_id is None:
            raise ValueError("The camera_id cannot be None")

        try:
            self.video_capture = cv2.VideoCapture(self.camera_id)
        except Exception as e:
            logging.error(f"Error while initializing the video capture: {e}")
            raise e

    def step(self) -> None:
        """Writes the video frame to the shared memory"""
        ret, frame = self.video_capture.read()
        if not ret:
            raise RuntimeError("Failed to capture frame")

        self.shared_mem.video_frame = frame

    def deinit(self) -> None:
        # Release the video capture
        logging.info("Deinitializing VideoCapture")
        try:
            self.video_capture.release()
        except Exception as e:
            logging.error(f"Error while deinitializing the video capture: {e}")
            raise e
