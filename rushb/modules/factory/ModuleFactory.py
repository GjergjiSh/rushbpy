from rushb.modules.RBModule import RBModule
from rushb.modules.collection.ServoReader import ServoReader
from rushb.modules.collection.ServoWriter import ServoWriter
from rushb.modules.collection.KeyboardControls import KeyboardControls
from rushb.modules.collection.VideoViewer import VideoViewer
from rushb.modules.collection.VideoCapture import VideoCapture
from rushb.modules.collection.Publisher import Publisher
from rushb.modules.collection.Subscriber import Subscriber
from rushb.modules.collection.ObjectDetector import ObjectDetector
from rushb.modules.collection.JoyStickControls import JoyStickControls

from abc import ABC, abstractmethod


class ModuleFactory(ABC):
    """ Base Factory class for creating modules """

    @abstractmethod
    def create_module(self, **kwargs) -> RBModule:
        pass


class ServoReaderFactory(ModuleFactory):
    def create_module(self, **kwargs) -> RBModule:
        """ Create a ServoReader module """
        return ServoReader(**kwargs)


class ServoWriterFactory(ModuleFactory):
    def create_module(self, **kwargs) -> RBModule:
        """ Create a ServoWriter module """
        return ServoWriter(**kwargs)


class KeyboardControlFactory(ModuleFactory):
    def create_module(self, **kwargs) -> RBModule:
        """ Create a KeyboardControl module """
        return KeyboardControls(**kwargs)


class VideoViewerFactory(ModuleFactory):
    def create_module(self, **kwargs) -> RBModule:
        """ Create a VideoViewer module """
        return VideoViewer(**kwargs)


class VideoCaptureFactory(ModuleFactory):
    def create_module(self, **kwargs) -> RBModule:
        """ Create a VideoCapture module """
        return VideoCapture(**kwargs)


class PublisherFactory(ModuleFactory):
    def create_module(self, **kwargs) -> RBModule:
        """ Create a Publisher module """
        return Publisher(**kwargs)


class SubscriberFactory(ModuleFactory):
    def create_module(self, **kwargs) -> RBModule:
        """ Create a Subscriber module """
        return Subscriber(**kwargs)


class ObjectDetectorFactory(ModuleFactory):
    def create_module(self, **kwargs) -> RBModule:
        """ Create a ObjectDetector module """
        return ObjectDetector(**kwargs)


class JoyStickControllerFactory(ModuleFactory):
    def create_module(self, **kwargs) -> RBModule:
        """ Create a JoyStickControls module """
        return JoyStickControls(**kwargs)


def make_module(module_type: str, **kwargs) -> RBModule:
    """ Create a module based on the module type and assign parameters """
    factories: dict[str, ModuleFactory] = {
        "ServoReader": ServoReaderFactory(),
        "ServoWriter": ServoWriterFactory(),
        "KeyboardControls": KeyboardControlFactory(),
        "VideoViewer": VideoViewerFactory(),
        "VideoCapture": VideoCaptureFactory(),
        "Publisher": PublisherFactory(),
        "Subscriber": SubscriberFactory(),
        "ObjectDetector": ObjectDetectorFactory(),
        "JoyStickControls": JoyStickControllerFactory()
    }

    if module_type in factories:
        return factories[module_type].create_module(**kwargs)
    else:
        raise ValueError("Unsupported module type")
