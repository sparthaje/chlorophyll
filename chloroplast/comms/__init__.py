# Shreepa Parthaje

from serial import Serial

from .helper import get_port
from .packet import Packet
from .printer import log
from .reader import SerialReader
from .writer import SerialWriter, DebugWriter


class Comms:

    def serial_config(self, comm_codes):
        if not self.serial_port:
            return

        if self.settings['DEBUG']:
            log(self, 'SUCCESS')

        serial = Serial(port=self.serial_port, baudrate=self.baudrate, write_timeout=0)

        serial_reader = SerialReader(serial, comm_codes['READ'])
        serial_reader.start()

        serial_writer = SerialWriter(serial, comm_codes['WRITE'])

        if not self.settings['PRODUCTION']:
            debug_writer = DebugWriter(serial)
            debug_writer.start()
            return serial, serial_reader, serial_writer, debug_writer

        return serial, serial_reader, serial_writer, None

    def __init__(self, settings, baudrate, comm_codes):
        self.settings = settings
        self.comm_codes = comm_codes
        self.baudrate = baudrate
        self.serial_port = get_port(settings)

        serial_config = self.serial_config(comm_codes)
        if serial_config:
            self.serial, self.reader, self.writer, self.debug_writer = serial_config
        else:
            self.serial = None

    def __str__(self):
        return f'On port {self.serial_port} at a baudrate of {self.baudrate}'

    def state_change(self, path, data):
        location = path.split("/")[1]
        fixture = path.split("/")[2]

        data_packet = Packet(location, fixture, data, self.comm_codes)
        if self.settings['DEBUG']:
            log(data_packet, 'PYTHON')

        if self.serial:
            self.writer.write_packet(data_packet)
        elif self.settings['DEBUG']:
            log('No arduino connected!\n', 'WARNING')

    def shutdown(self):
        if self.serial:
            self.serial.close()
