import keyboard
import logging
import datetime

from rushb.modules.RBModule import *


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
        # Log the button mapping and the x and y speed
        logging.info("Initializing KeyboardControls")
        logging.info(f"KeyboardControls x speed: {self.x_speed} y speed: {self.y_speed}")
        logging.info(f"Keyboard button mapping: {self.button_mapping}")

    def step(self) -> None:
        self.__get_keyboard_input()
        self.__update_servo_values()

    def deinit(self) -> None:
        logging.info("Deinitializing KeyboardControls")

    def __get_keyboard_input(self) -> None:
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

    def __update_servo_values(self) -> None:
        """"Calculate the position of the servos based on the directional values
            and update the servo values in the shared memory"""

        # TODO Fixme
        # Limit the values of the left and right track between 0 and 180
        self.left_track = max(0, min(self.left_track, 180))
        self.right_track = max(0, min(self.right_track, 180))

        # Update the servo values in the shared memory
        self.shared_mem.servo_vals.values[0] = self.left_track
        self.shared_mem.servo_vals.values[1] = self.right_track

        # Update the last update time
        self.shared_mem.servo_vals.last_update = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
