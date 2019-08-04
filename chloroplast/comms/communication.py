# Shreepa Parthaje

from serial import Serial

from .helper import list_serial_ports
from .packet import Packet
from .reader import SerialReader
from .writer import SerialWriter, DebugWriter


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

    def serial_config(self, comm_codes):
        if not self.serial_port:
            return

        if self.settings['DEBUG']:
            print(self)

        serial = Serial(port=self.serial_port, baudrate=self.baudrate, write_timeout=0)

        reader = SerialReader(serial, comm_codes['READ'])
        reader.start()

        writer = SerialWriter(serial, comm_codes['WRITE'])

        if not self.settings['PRODUCTION']:
            debug_writer = DebugWriter(serial)
            debug_writer.start()
            return serial, reader, writer, debug_writer

        return serial, reader, writer, None

    def __init__(self, settings, baudrate, comm_codes):
        self.packet_queue = []
        self.settings = settings
        self.baudrate = baudrate
        self.serial_port = self.get_port(settings)
        self.serial, self.reader, self.writer, self.debug_writer = self.serial_config(comm_codes)

    def __str__(self):
        return f'On port {self.serial_port} at a baudrate of {self.baudrate}'

    def state_change(self, path, data):
        location = path.split("/")[1]
        fixture = path.split("/")[2]

        packet = Packet(location, fixture, data)
        if self.settings["DEBUG"]:
            print(packet)

        self.packet_queue.append(packet)
