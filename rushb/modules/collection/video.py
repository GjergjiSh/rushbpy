import cv2

from rushb.modules.rb_module import *


class VideoCapture(RBModule):
    """VideoCapture is a class that captures the video feed from the webcam
     and writes it to the shared memory"""

    video_capture: cv2.VideoCapture
    camera_id: int

    def __init__(self, **kwargs) -> None:
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

    def step(self, shared_mem: SharedMem) -> SharedMem:
        """Writes the video frame to the shared memory"""
        ret, frame = self.video_capture.read()
        if not ret:
            raise RuntimeError("Failed to capture frame")

        shared_mem.video_frame = frame
        return shared_mem

    def deinit(self) -> None:
        # Release the video capture
        logging.info("Deinitializing VideoCapture")
        try:
            self.video_capture.release()
        except Exception as e:
            logging.error(f"Error while deinitializing the video capture: {e}")
            raise e


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

    def step(self, shared_mem: SharedMem) -> SharedMem:
        # Get the video frame from the shared memory
        frame = shared_mem.video_frame

        # Check if the frame is empty
        if frame is None:
            logging.warning("Video frame is empty")
            return

        # Show the frame
        cv2.imshow("Video", frame)
        cv2.waitKey(1)

        return shared_mem

    def deinit(self) -> None:
        # Close the display window
        try:
            logging.info("Deinitializing VideoViewer")
            cv2.destroyAllWindows()
        except Exception as e:
            logging.error(f"Error while deinitializing the video viewer: {e}")
            raise e
