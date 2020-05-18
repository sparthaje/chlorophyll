# Shreepa Parthaje

import RPi.GPIO as GPIO

from .reader import InputReader


class Pi:

    def __init__(self, pin_map):
        GPIO.setmode(GPIO.BOARD)

        self.pin_map = pin_map
        self.output_pin_info = pin_map["OUTPUT"]
        self.input_pin_info = pin_map["INPUT"]

        for location in self.output_pin_info:
            for fixture in self.output_pin_info[location]:
                GPIO.setup(self.output_pin_info[location][fixture], GPIO.OUT)

        pins = []
        for location in self.input_pin_info:
            for fixture in self.input_pin_info[location]:
                GPIO.setup(self.input_pin_info[location][fixture], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                pins.append(self.input_pin_info[location][fixture])

        self.reader = InputReader(pins, self.input_pin_info)

    def start(self):
        self.reader.start()

    def update_relay(self, path, data):
        """ Takes a path from the database along with the data and writes it to the GPIO pins """

        location = path.split("/")[1]
        fixture = path.split("/")[2]
        pin = self.output_pin_info[location][fixture]
        GPIO.output(pin, data)
