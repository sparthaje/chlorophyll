# Shreepa Parthaje

from .arduino import get_serial_ports
from .packet import Packet


class Comms:
    def __init__(self, settings, baudrate):
        self.packet_queue = []
        self.settings = settings
        self.baudrate = baudrate

        ports = get_serial_ports()

        if len(ports) == 0:
            if settings["PRODUCTION"]:
                raise OSError("No serial device connected")
            else:
                if settings["DEBUG"]:
                    print("No serial device connected")
                self.serial_port = None
                return

        if len(ports) == 1:
            port_index = 0
        else:
            port_index = int(input(f"Choose which serial port to use: {ports}: "))

        self.serial_port = ports[port_index]

    def state_change(self, path, data):
        location = path.split("/")[1]
        fixture = path.split("/")[2]

        packet = Packet(location, fixture, data)
        if self.settings["DEBUG"]:
            print(packet)

        self.packet_queue.append(packet)
