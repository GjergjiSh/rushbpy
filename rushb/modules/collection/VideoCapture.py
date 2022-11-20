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
        self.video_capture = cv2.VideoCapture(self.camera_id)

    def step(self) -> None:
        """Writes the video frame to the shared memory"""
        ret, frame = self.video_capture.read()
        if not ret:
            raise RuntimeError("Failed to capture frame")

        self.shared_mem.video_frame = frame

    def deinit(self) -> None:
        # Release the video capture
        logging.info("Deinitializing VideoCapture")
        self.video_capture.release()
