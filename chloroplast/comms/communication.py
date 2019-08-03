# Shreepa Parthaje

from .helper import list_serial_ports
from .packet import Packet


class Comms:
    @staticmethod
    def get_port(settings):
        ports = list_serial_ports(settings['DEBUG'])

        if len(ports) == 0:
            if settings['PRODUCTION']:
                raise OSError('No serial device connected')
            else:
                if settings['DEBUG']:
                    print('No serial device connected')
                return None

        if len(ports) == 1:
            port_index = 0
        else:
            port_index = int(input(f'Choose which serial port to use: {ports}: '))

        return ports[port_index]

    def __init__(self, settings, baudrate):
        self.packet_queue = []
        self.settings = settings
        self.baudrate = baudrate
        self.serial_port = self.get_port(settings)

        if self.serial_port and settings['DEBUG']:
            print(self)

    def __str__(self):
        return f'On port {self.serial_port} at a baudrate of {self.baudrate}'

    def state_change(self, path, data):
        location = path.split("/")[1]
        fixture = path.split("/")[2]

        packet = Packet(location, fixture, data)
        if self.settings["DEBUG"]:
            print(packet)

        self.packet_queue.append(packet)
