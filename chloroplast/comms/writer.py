# Shreepa Parthaje

from threading import Thread


class DebugWriter(Thread):
    def __init__(self, serial):
        Thread.__init__(self)
        self.serial = serial

    def run(self):
        while True:
            message = input()
            if message == '0':
                self.serial.write(bytes([int(input())]))


class SerialWriter:
    def __init__(self, serial, comm_codes):
        self.serial = serial
        self.comm_codes = comm_codes

    def write_packet(self, packet):
        for byte in packet.data():
            self.serial.write(byte)
