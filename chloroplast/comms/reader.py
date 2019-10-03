# Shreepa Parthaje

from threading import Thread
from time import sleep

from .printer import log


class SerialReader(Thread):
    def __init__(self, serial, comm_codes, input_pins, debug):
        Thread.__init__(self)
        self.serial = serial
        self.comm_codes = comm_codes
        self.input_pins = input_pins
        self.debug = debug
        self.handler = None

    def run(self):
        while True:
            data = self.serial.read()
            header = ord(data)

            if (
                header == self.comm_codes["DEBUG_HEADER"]
                or header == self.comm_codes["ERROR_HEADER"]
            ):
                message_length = ord(self.serial.read())
                message = ""
                for i in range(message_length):
                    message += self.serial.read().decode()
                footer = ord(self.serial.read())
                if not footer == self.comm_codes["FOOTER"]:
                    raise RuntimeError("Footer byte not printed, possibly corrupted")
                if header == self.comm_codes["ERROR_HEADER"]:
                    log(message + "\n", "ARDUINO ERROR")
                elif self.debug:
                    log(message + "\n", "ARDUINO")

            elif header == self.comm_codes["STATE_HEADER"]:
                pin = self.serial.read()

                location, fixture = "", ""
                for l in self.input_pins:
                    for f in self.input_pins[l]:
                        if self.input_pins[l][f] == pin:
                            location, fixture = l, f
                if location == "":
                    continue
                if self.handler:
                    self.handler(location, fixture)

                footer = ord(self.serial.read())
                if not footer == self.comm_codes["FOOTER"]:
                    raise RuntimeError("Footer byte not printed, possibly corrupted")

            elif self.debug:
                log(f"Data: {data}, Header: {header}\n", "ARDUINO")

            sleep(0.5)
