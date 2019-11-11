# Shreepa Parthaje

from threading import Thread

import RPi.GPIO as GPIO


class InputReader(Thread):
    def __init__(self, pins, input_pins):
        Thread.__init__(self)
        self.pins = pins
        self.input_pins = input_pins
        self.states = dict([(pin, GPIO.input(pin)) for pin in pins])
        self.handler = None

    def run(self):
        while True:
            for pin in self.pins:
                old = self.states[pin]
                current = GPIO.input(pin)
                if not old and current:
                    # Just clicked
                    if self.handler is None:
                        continue

                    args = ()
                    for location in self.input_pins:
                        for fixture in self.input_pins[location]:
                            if self.input_pins[location][fixture] == pin:
                                args = (location, fixture)
                    self.handler(*args)

                self.states[pin] = current
