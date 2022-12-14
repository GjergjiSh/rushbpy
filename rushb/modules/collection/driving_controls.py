import logging
from numpy import interp
import datetime
from os import environ
import keyboard

from rushb.modules.rb_module import *
from rushb.sharedmem.shared_mem import Servos

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

    def step(self, shared_mem: SharedMem) -> SharedMem:
        self.get_gamepad_input()
        shared_mem.servo_vals.values[Servos.LEFT] = int(self.left_stick)
        shared_mem.servo_vals.values[Servos.RIGHT] = int(self.right_stick)
        shared_mem.servo_vals.last_update = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        return shared_mem

    def deinit(self) -> None:
        # Release the joystick and pygame
        logging.info("Deinitializing JoyStickControls")
        try:
            pygame.joystick.quit()
            pygame.quit()
        except pygame.error:
            raise RuntimeError("Could not deinitialize joystick")

    def get_gamepad_input(self) -> None:
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


class KeyboardControls(RBModule):
    """KeyboardControls is a module that controls the servos using the keyboard"""

    def __init__(self, **kwargs) -> None:
        self.button_mapping: dict[str, str] = {
            "up": kwargs.get("up"),
            "down": kwargs.get("down"),
            "left": kwargs.get("left"),
            "right": kwargs.get("right"),
        }

        self.x_speed: float = kwargs.get("x_speed")
        self.y_speed: float = kwargs.get("y_speed")

        self.right_track = 90
        self.left_track = 90

    def init(self) -> None:
        # Check if any of the button mappings is None
        if None in self.button_mapping.values():
            raise ValueError("The button mappings cannot be None")

        # Check if the x_speed and y_speed are not None
        if self.x_speed is None or self.y_speed is None:
            raise ValueError("The x_speed and y_speed cannot be None")

        # Log the button mapping and the x and y speed
        logging.info("Initializing KeyboardControls")
        logging.info(f"KeyboardControls x speed: {self.x_speed} y speed: {self.y_speed}")
        logging.info(f"Keyboard button mapping: {self.button_mapping}")

    def step(self, shared_mem: SharedMem) -> SharedMem:
        self.get_keyboard_input()
        return self.update_servo_values(shared_mem)

    def deinit(self) -> None:
        logging.info("Deinitializing KeyboardControls")

    def get_keyboard_input(self) -> None:
        """"Get the pressed key with the keyboard module and update the directional values"""

        # up pressed
        if keyboard.is_pressed(self.button_mapping["up"]):
            self.left_track += self.y_speed
            self.right_track += self.y_speed
        # down pressed
        if keyboard.is_pressed(self.button_mapping["down"]):
            self.left_track -= self.y_speed
            self.right_track -= self.y_speed

        # left pressed
        if keyboard.is_pressed(self.button_mapping["left"]):
            self.left_track -= self.x_speed
            self.right_track += self.x_speed
        # right pressed
        if keyboard.is_pressed(self.button_mapping["right"]):
            self.left_track += self.x_speed
            self.right_track -= self.x_speed

        if keyboard.is_pressed("space"):
            self.left_track = 90
            self.right_track = 90

        # Log the directional values
        # logging.debug(f"KeyboardControls directional values: {self.directional_values}")

    def update_servo_values(self, shared_mem: SharedMem) -> SharedMem:
        """"Calculate the position of the servos based on the directional values
            and update the servo values in the shared memory"""

        # TODO Fixme
        # Limit the values of the left and right track between 0 and 180
        self.left_track = max(0, min(self.left_track, 180))
        self.right_track = max(0, min(self.right_track, 180))

        # Update the servo values in the shared memory
        shared_mem.servo_vals.values[Servos.LEFT] = self.left_track
        shared_mem.servo_vals.values[Servos.RIGHT] = self.right_track

        # Update the last update time
        shared_mem.servo_vals.last_update = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        return shared_mem
