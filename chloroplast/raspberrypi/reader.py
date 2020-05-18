# Shreepa Parthaje

from threading import Thread

import RPi.GPIO as GPIO
from firebase_admin import db


class InputReader(Thread):
    def __init__(self, input_pins, input_pins_info):
        Thread.__init__(self)
        self.input_pins = input_pins
        self.input_pins_info = input_pins_info
        self.states = {pin: GPIO.input(pin) for pin in input_pins}

    def run(self):
        while True:
            for pin in self.input_pins:
                old = self.states[pin]
                current = GPIO.input(pin)

                if not old and current:  # Wasn't on before and is on now
                    location, fixture = '', ''  # Find the location / fixture that the input pin corresponds to
                    for loc in self.input_pins_info:
                        for fix in self.input_pins_info[loc]:
                            if self.input_pins_info[loc][fix] == pin:
                                location, fixture = loc, fix

                    db_reference = db.reference("/state").child(location).child(fixture)
                    db_reference.set(not db_reference.get())

                self.states[pin] = current
