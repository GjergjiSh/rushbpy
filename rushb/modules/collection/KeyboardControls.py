import keyboard
import logging

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

        # Dictionary of the current directional values
        self.directional_values: dict[str, int] = {
            "x": 90,
            "y": 90,
        }

        self.x_speed: int = kwargs.get("x_speed")
        self.y_speed: int = kwargs.get("y_speed")

    def init(self) -> None:
        # Log the button mapping and the x and y speed
        logging.info("Initializing KeyboardControls")
        logging.info(f"KeyboardControls x speed: {self.x_speed} y speed: {self.y_speed}")
        logging.info(f"Keyboard button mapping: {self.button_mapping}")

    def step(self) -> None:
        # Read the pressed key with the keyboard module and update the servo values
        # in the shared memory

        # up pressed
        if keyboard.is_pressed(self.button_mapping["up"]):
            self.directional_values["y"] += self.y_speed
        # down pressed
        elif keyboard.is_pressed(self.button_mapping["down"]):
            self.directional_values["y"] -= self.y_speed
        # left pressed
        elif keyboard.is_pressed(self.button_mapping["left"]):
            self.directional_values["x"] -= self.y_speed
        # right pressed
        elif keyboard.is_pressed(self.button_mapping["right"]):
            self.directional_values["x"] += self.y_speed
        # no key pressed
        else:
            self.directional_values["x"] = 90
            self.directional_values["y"] = 90

        # Limit the directional values to the range [0, 180]
        self.directional_values["x"] = max(0, min(180, self.directional_values["x"]))
        self.directional_values["y"] = max(0, min(180, self.directional_values["y"]))

        # Log the directional values
        logging.info(f"KeyboardControls directional values: {self.directional_values}")

        # Calculate the position of the servos based on the directional values
        # and update the servo values in the shared memory

    def deinit(self) -> None:
        logging.info("Deinitializing KeyboardControls")
