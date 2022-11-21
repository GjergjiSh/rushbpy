import logging
from numpy import interp
import datetime
from os import environ

from rushb.modules.RBModule import *

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

class JoyStickControls(RBModule):
    def __init__(self, **kwargs) -> None:
        self.joystick_id = kwargs.get("joystick_id")
        self.joystick = None
        self.right_stick = 0
        self.left_stick = 0

    def init(self) -> None:
        # Check if the joystick id is not None
        if self.joystick_id is None:
            raise ValueError("The joystick_id cannot be None")

        # Initialize pygame and the joystick module
        logging.info("Initializing JoyStickControls")
        pygame.init()
        pygame.joystick.init()
        try:
            self.joystick = pygame.joystick.Joystick(self.joystick_id)
            self.joystick.init()
        except pygame.error:
            raise RuntimeError("Could not initialize joystick")

    def step(self) -> None:
        self.__get_gamepad_input()
        self.shared_mem.servo_vals.values[0] = int(self.left_stick)
        self.shared_mem.servo_vals.values[1] = int(self.right_stick)
        self.shared_mem.servo_vals.last_update = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def deinit(self) -> None:
        # Release the joystick and pygame
        logging.info("Deinitializing JoyStickControls")
        try:
            pygame.joystick.quit()
            pygame.quit()
        except pygame.error:
            raise RuntimeError("Could not deinitialize joystick")

    def __get_gamepad_input(self) -> None:
        # Read the event queue
        try:
            pygame.event.get()
        except pygame.error:
            raise RuntimeError("Could not read event queue")

        # Get the vertical positions of the left and right joysticks
        self.left_stick = -1 * round(self.joystick.get_axis(1), 1)
        self.right_stick = -1 * round(self.joystick.get_axis(3), 1)
        # Interpolate the values to the range of the servo
        self.left_stick = interp(self.left_stick, [-1, 1], [0, 180])
        self.right_stick = interp(self.right_stick, [-1, 1], [0, 180])