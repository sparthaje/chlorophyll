# Shreepa Parthaje

from ..settings import *
from .packet import Packet
from .arduino import get_serial_ports


class Comms:
    def __init__(self):
        ports = get_serial_ports()

        if len(ports) == 0:
            if PRODUCTION:
                raise OSError("No serial device connected")
            else:
                print("No serial device connected")

        if len(ports) == 1:
            port_index = 0
        else:
            port_index = int(input(f"Choose which serial port to use: {ports}: "))

        self.serial_port = ports[port_index]
        self.packet_queue = []

    def state_change(self, path, data):
        location = path.split("/")[1]
        fixture = path.split("/")[2]

        packet = Packet(location, fixture, data)
        self.packet_queue.append(packet)
