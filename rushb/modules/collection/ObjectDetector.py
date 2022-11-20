import logging
from typing import Any

import cv2
import numpy as np
import os
import tensorflow as tf
from tensorflow.python.keras.utils.data_utils import get_file

from rushb.modules.RBModule import *


class ObjectDetector(RBModule):
    """ObjectDetector is a class that detects objects in an image using a pre-trained model."""

    def __init__(self, **kwargs) -> None:
        self.model_url = kwargs.get("model_url")
        self.labels_path = kwargs.get("labels_path")
        self.cache_dir = kwargs.get("cache_dir")
        self.iou_threshold = kwargs.get("iou_threshold")
        self.confidence_threshold = kwargs.get("confidence_threshold")
        self.max_detections = kwargs.get("max_detections")

        self.class_names = []
        self.class_colors = []

        self.model_name = None
        self.detection_model = None

    def init(self) -> None:
        logging.info("Initializing ObjectDetector")
        self.read_classes()
        self.download_model()
        self.load_model()

    def step(self) -> None:
        self.shared_mem.video_frame = self.predict(self.shared_mem.video_frame)

    def deinit(self) -> None:
        pass

    def read_classes(self) -> None:
        """Reads the classes from the labels file and
        creates a list of colors for each class"""

        logging.info(f"Reading classes from {self.labels_path}")
        with open(self.labels_path, "r") as f:
            self.class_names = [cname.strip() for cname in f.readlines()]

        self.class_colors = np.random.uniform(0, 255, size=(len(self.class_names), 3))

    def download_model(self) -> None:
        """Downloads the model from the TensorFlow model zoo
        and extracts it to the cache directory. If the model
        is already present in the cache dir, it will not
        be downloaded again"""

        file_name = os.path.basename(self.model_url)
        self.model_name = file_name[:file_name.index(".")]

        self.cache_dir = "./pretrained_models"
        os.makedirs(self.cache_dir, exist_ok=True)

        get_file(file_name, origin=self.model_url, cache_dir=self.cache_dir,
                 cache_subdir=self.model_name, extract=True)

    def load_model(self) -> None:
        """Loads the model from the cache directory in a variable"""

        model_path = os.path.join(self.cache_dir, self.model_name, self.model_name, "saved_model")
        logging.info(f"Loading model from {model_path}")
        tf.keras.backend.clear_session()
        self.detection_model = tf.saved_model.load(model_path)

    def predict(self, image):
        """Predicts the objects in the image using the model"""

        all_predictions, class_indexes, class_scores = self.__feed_forward_image(image)
        confident_predictions = self.__nms(all_predictions, class_scores)
        image = self.__draw_bounding_boxes(all_predictions, confident_predictions,
                                           class_scores, class_indexes, image)
        return image

    def __feed_forward_image(self, image) -> tuple[Any, Any, Any]:
        """Feed the frame to the model and get the predictions"""

        input_tensor = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        input_tensor = tf.convert_to_tensor(input_tensor, dtype=tf.uint8)
        input_tensor = input_tensor[tf.newaxis, ...]

        detections = self.detection_model(input_tensor)

        bounding_boxes = detections['detection_boxes'][0].numpy()
        class_indexes = detections['detection_classes'][0].numpy().astype(np.int32)
        class_scores = detections['detection_scores'][0].numpy()

        logging.debug(f"Detection count: {len(bounding_boxes)}")
        return bounding_boxes, class_indexes, class_scores

    def __nms(self, bounding_boxes, class_scores):
        """Non-maximum suppression to remove overlapping bounding boxes"""

        confident_predictions = tf.image.non_max_suppression(
            bounding_boxes, class_scores, self.max_detections,
            self.iou_threshold,
            self.confidence_threshold)

        logging.debug(f"Confident predictions: {len(confident_predictions)}")

        return confident_predictions

    def __draw_bounding_boxes(self, all_predictions, confident_predictions,
                              class_scores, class_indexes, image):
        """Draw bounding boxes of the confident predictions on the image"""

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

        return image
