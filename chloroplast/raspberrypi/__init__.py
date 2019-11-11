# Shreepa Parthaje

import RPi.GPIO as GPIO

from .reader import InputReader


class Pi:

    def __init__(self, settings, pin_map):
        GPIO.setmode(GPIO.BOARD)

        self.settings = settings
        self.pin_map = pin_map
        self.output_pins = pin_map["OUTPUT"]
        self.input_pins = pin_map["INPUT"]

        pins = self.configure_pins()

        self.reader = InputReader(pins, self.input_pins)
        self.reader.start()

    def configure_pins(self):
        for location in self.output_pins:
            for fixture in self.output_pins[location]:
                GPIO.setup(self.output_pins[location][fixture], GPIO.OUT)

        pins = []
        for location in self.input_pins:
            for fixture in self.input_pins[location]:
                GPIO.setup(self.input_pins[location][fixture], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                pins.append(self.input_pins[location][fixture])
        return pins

    def state_change(self, path, data):
        """ Takes a path from the database along with the data and writes it to the GPIO pins """

        location = path.split("/")[1]
        fixture = path.split("/")[2]
        pin = self.output_pins[location][fixture]
        GPIO.output(pin, data)
