# Shreepa Parthaje

from .packet import Packet

SERIAL = "test"


def state_change(path, data):
    location = path.split("/")[1]
    fixture = path.split("/")[2]

    packet = Packet(location, fixture, data)
    print(SERIAL)
    print(packet)


def set_serial(serial):
    global SERIAL
    SERIAL = serial
