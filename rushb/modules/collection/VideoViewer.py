import cv2
import logging
from rushb.modules.RBModule import *


class VideoViewer(RBModule):
    """VideoViewer is a class that displays the video feed from the shared memory"""

    def __init__(self, **kwargs) -> None:
        # Get the window size from the kwargs
        self.height = kwargs.get("height")
        self.width = kwargs.get("width")

    def init(self) -> None:
        logging.info("Initializing VideoViewer")
        # Initialize the display window
        cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
        # Set the window size
        cv2.resizeWindow("Video", self.width, self.height)

    def step(self) -> None:
        # Get the video frame from the shared memory
        frame = self.shared_mem.video_frame

        # Check if the frame is empty
        if frame is None:
            logging.warning("Video frame is empty")
            return

        # Show the frame
        cv2.imshow("Video", frame)
        cv2.waitKey(1)

    def deinit(self) -> None:
        # Close the display window
        logging.info("Deinitializing VideoViewer")
        cv2.destroyAllWindows()
