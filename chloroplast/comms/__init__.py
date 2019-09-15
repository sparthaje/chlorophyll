# Shreepa Parthaje

from serial import Serial

from .helper import get_port
from .packet import RelayPacket, PinPacket
from .printer import log
from .reader import SerialReader
from .writer import SerialWriter, DebugWriter


class Comms:

    def serial_config(self, comm_codes):
        """ Creates a Serial, SerialReader, SerialWriter, DebugWriter based on given preferences """

        if not self.serial_port:
            return

        if self.settings['DEBUG']:
            log(self, 'SUCCESS')

        serial = Serial(port=self.serial_port, baudrate=self.baudrate, write_timeout=0)

        serial_reader = SerialReader(serial, comm_codes['READ'], comm_codes['INPUT_PINS'], self.settings['DEBUG'])
        serial_reader.start()

        serial_writer = SerialWriter(serial, comm_codes['WRITE'])

        if not self.settings['PRODUCTION']:
            debug_writer = DebugWriter(serial)
            debug_writer.start()
            return serial, serial_reader, serial_writer, debug_writer

        return serial, serial_reader, serial_writer, None

    def __init__(self, settings, baudrate, comm_codes):
        """ Creates a Comms with given environment settings and communication codes at a given baudrate on a port """

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

    def set_pin_mode(self):
        """ Tells arduino to configure specific pins (defined by OUTPUT_PINS and INPUT_PINS in comm_codes)
        to OUTPUT/INPUT"""

        for location in self.comm_codes['OUTPUT_PINS']:
            for fixture in self.comm_codes['OUTPUT_PINS'][location]:
                pin_packet = PinPacket(self.comm_codes['OUTPUT_PINS'][location][fixture], self.comm_codes)
                self.writer.write_packet(pin_packet)

        for location in self.comm_codes['INPUT_PINS']:
            for index, fixture in enumerate(self.comm_codes['INPUT_PINS'][location]):
                pin_packet = PinPacket(self.comm_codes['INPUT_PINS'][location][fixture], self.comm_codes, index)
                self.writer.write_packet(pin_packet)

    def state_change(self, path, data):
        """ Takes a path from the database along with the data and writes it to the arduino to signal the relay """

        location = path.split("/")[1]
        fixture = path.split("/")[2]

        data_packet = RelayPacket(location, fixture, data, self.comm_codes)
        if self.settings['DEBUG']:
            log(data_packet, 'PYTHON')

        if self.serial:
            self.writer.write_packet(data_packet)
        elif self.settings['DEBUG']:
            log('No arduino connected!\n', 'WARNING')

    def shutdown(self):
        """ Closes the port and signals to the arduino that the port is closing """

        if self.serial:
            self.writer.signal_close()
            self.serial.close()
