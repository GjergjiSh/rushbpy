import logging
from typing import Any

import cv2
import numpy as np
import os
import tensorflow as tf
from tensorflow.python.keras.utils.data_utils import get_file

from rushb.modules.rb_module import *


class ObjectDetector(RBModule):
    """ObjectDetector is a class that detects objects in an image using a pre-trained model."""

    model_url: str
    labels_path: str
    cache_dir: str
    iou_threshold: float
    confidence_threshold: float
    max_detections: int
    class_names: list[str]
    class_colors: list[tuple[int, int, int]]

    model_name: str
    detection_model: tf.saved_model.load

    def __init__(self, **kwargs) -> None:
        self.model_url = kwargs.get("model_url")
        self.labels_path = kwargs.get("labels_path")
        self.cache_dir = kwargs.get("cache_dir")
        self.iou_threshold = kwargs.get("iou_threshold")
        self.confidence_threshold = kwargs.get("confidence_threshold")
        self.max_detections = kwargs.get("max_detections")

    def init(self) -> None:
        logging.info("Initializing ObjectDetector")
        self.read_classes()
        self.download_model()
        self.load_model()

    def step(self, shared_mem: SharedMem) -> SharedMem:
        shared_mem.video_frame = self.predict(shared_mem.video_frame)
        return shared_mem

    def deinit(self) -> None:
        pass

    def read_classes(self) -> None:
        """Reads the classes from the labels file and
        creates a list of colors for each class"""

        # Check if the labels path is not None
        if self.labels_path is None:
            raise ValueError("Labels path is not set")

        # Check if the labels file exists
        if not os.path.exists(self.labels_path):
            raise FileNotFoundError(f"Labels file not found at {self.labels_path}")

        self.class_names = []
        self.class_colors = []

        try:
            logging.info(f"Reading classes from {self.labels_path}")
            with open(self.labels_path, "r") as f:
                self.class_names = [cname.strip() for cname in f.readlines()]

            self.class_colors = np.random.uniform(0, 255, size=(len(self.class_names), 3))
        except Exception as e:
            logging.error(f"Error reading classes from {self.labels_path}")
            raise e

    def download_model(self) -> None:
        """Downloads the model from the TensorFlow model zoo
        and extracts it to the cache directory. If the model
        is already present in the cache dir, it will not
        be downloaded again"""

        # Check if the model url is valid
        if not self.model_url:
            raise ValueError("Model URL is not valid")

        file_name = os.path.basename(self.model_url)
        self.model_name = file_name[:file_name.index(".")]

        # Check if the cache directory is not None
        if self.cache_dir is None:
            raise ValueError("Cache directory is not set")

        os.makedirs(self.cache_dir, exist_ok=True)

        try:
            get_file(file_name, origin=self.model_url, cache_dir=self.cache_dir,
                     cache_subdir=self.model_name, extract=True)
        except Exception as e:
            logging.error(f"Error downloading model from {self.model_url}")
            raise e

    def load_model(self) -> None:
        """Loads the model from the cache directory in a variable"""

        model_path = os.path.join(self.cache_dir, self.model_name, self.model_name, "saved_model")

        # Check if the model exists
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")

        try:
            logging.info(f"Loading model from {model_path}")
            tf.keras.backend.clear_session()
            self.detection_model = tf.saved_model.load(model_path)
        except Exception as e:
            logging.error(f"Error loading model from {model_path}")
            raise e

    def predict(self, image):
        """Predicts the objects in the image using the model"""

        all_predictions, class_indexes, class_scores = self.feed_forward_image(image)
        confident_predictions = self.nms(all_predictions, class_scores)
        image = self.draw_bounding_boxes(all_predictions, confident_predictions,
                                           class_scores, class_indexes, image)
        return image

    def feed_forward_image(self, image) -> tuple[Any, Any, Any]:
        """Feed the frame to the model and get the predictions"""

        try:
            input_tensor = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            input_tensor = tf.convert_to_tensor(input_tensor, dtype=tf.uint8)
            input_tensor = input_tensor[tf.newaxis, ...]
        except Exception as e:
            logging.error("Error converting image to tensor")
            raise e

        try:
            detections = self.detection_model(input_tensor)
            bounding_boxes = detections['detection_boxes'][0].numpy()
            class_indexes = detections['detection_classes'][0].numpy().astype(np.int32)
            class_scores = detections['detection_scores'][0].numpy()
        except Exception as e:
            logging.error("Error getting predictions from model")
            raise e

        logging.debug(f"Detection count: {len(bounding_boxes)}")
        return bounding_boxes, class_indexes, class_scores

    def nms(self, bounding_boxes, class_scores):
        """Non-maximum suppression to remove overlapping bounding boxes"""

        # Check if the max detections is not None
        if self.max_detections is None:
            raise ValueError("Max detections is not set")

        # Check if the iou threshold is not None
        if self.iou_threshold is None:
            raise ValueError("IOU threshold is not set")

        # Check if the confidence threshold is not None
        if self.confidence_threshold is None:
            raise ValueError("Confidence threshold is not set")

        try:
            confident_predictions = tf.image.non_max_suppression(
                bounding_boxes, class_scores, self.max_detections,
                self.iou_threshold,
                self.confidence_threshold)
        except Exception as e:
            logging.error("Error performing NMS")
            raise e

        logging.debug(f"Confident predictions: {len(confident_predictions)}")

        return confident_predictions

    def draw_bounding_boxes(self, all_predictions, confident_predictions,
                              class_scores, class_indexes, image):
        """Draw bounding boxes of the confident predictions on the image"""

        try:
            h, w, c = image.shape
            if len(confident_predictions) != 0:
                for i in confident_predictions:
                    bounding_box = tuple(all_predictions[i].tolist())
                    class_confidence = round(100 * class_scores[i])
                    class_index = class_indexes[i]
                    class_label = self.class_names[class_index - 1]
                    color = tuple(self.class_colors[class_index - 1])

                    # Text to be displayed on the bounding box
                    display_text = f"{class_label} {class_confidence}%"

                    # Coordinates of the bounding box
                    y_min, x_min, y_max, x_max = bounding_box
                    y_min, x_min, y_max, x_max = int(y_min * h), int(x_min * w), int(y_max * h), int(x_max * w)

                    # Draw the bounding box and the text
                    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)
                    cv2.putText(image, display_text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        except Exception as e:
            logging.error("Error drawing bounding boxes")
            raise e

        return image
