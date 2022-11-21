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
        # Check if the height and width are not None
        if self.height is None or self.width is None:
            raise ValueError("The height and width cannot be None")

        try:
            logging.info("Initializing VideoViewer")
            # Initialize the display window
            cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
            # Set the window size
            cv2.resizeWindow("Video", self.width, self.height)
        except Exception as e:
            logging.error(f"Error while initializing the video viewer: {e}")
            raise e

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
        try:
            logging.info("Deinitializing VideoViewer")
            cv2.destroyAllWindows()
        except Exception as e:
            logging.error(f"Error while deinitializing the video viewer: {e}")
            raise e
