# Shreepa Parthaje

from threading import Thread
from time import sleep

from .printer import log


class SerialReader(Thread):
    def __init__(self, serial, comm_codes):
        Thread.__init__(self)
        self.serial = serial
        self.comm_codes = comm_codes

    def run(self):
        while True:
            data = self.serial.read()
            header = ord(data)
            if header == self.comm_codes['DEBUG_HEADER'] or header == self.comm_codes['ERROR_HEADER']:
                message_length = ord(self.serial.read())
                message = ''
                for i in range(message_length):
                    message += self.serial.read().decode()
                footer = ord(self.serial.read())
                if not footer == self.comm_codes['FOOTER']:
                    raise RuntimeError('Footer byte not printed, possibly corrupted')
                if header == self.comm_codes['ERROR_HEADER']:
                    log(message + '\n', 'ARDUINO ERROR')
                else:
                    log(message + '\n', 'ARDUINO')
            else:
                log(f'Data: {data}, Header: {header}\n', 'ARDUINO')
            sleep(0.5)
