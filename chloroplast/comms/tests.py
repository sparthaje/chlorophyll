from serial import Serial

from pty import openpty
from os import ttyname, write, read
from time import sleep
from unittest import TestCase

from .packet import RelayPacket, PinPacket
from .reader import SerialReader
from .writer import SerialWriter

comm_codes = {
    "READ": {"DEBUG_HEADER": 100, "ERROR_HEADER": 25, "STATE_HEADER": 37, "FOOTER": 50},
    "WRITE": {
        "PACKET_HEADER": bytes([23]),
        "OUTPUT_HEADER": bytes([20]),
        "INPUT_HEADER": bytes([30]),
        "WRITE_FOOTER": bytes([32]),
        "SERIAL_CLOSE": bytes([40]),
    },
    "OUTPUT_PINS": {"CEILING": {"FAN": bytes([2]), "LIGHT": bytes([3])}},
    "INPUT_PINS": {"CEILING": {"FAN": bytes([4]), "LIGHT": bytes([7])}},
}


class TestPackets(TestCase):
    def test_relay_packet(self):
        self.assertEqual(
            [23, 2, 1, 32],
            [ord(x) for x in RelayPacket("CEILING", "FAN", True, comm_codes).data()],
        )
        self.assertEqual(
            [23, 2, 0, 32],
            [ord(x) for x in RelayPacket("CEILING", "FAN", False, comm_codes).data()],
        )
        self.assertEqual(
            [23, 3, 1, 32],
            [ord(x) for x in RelayPacket("CEILING", "LIGHT", True, comm_codes).data()],
        )
        self.assertEqual(
            [23, 3, 0, 32],
            [ord(x) for x in RelayPacket("CEILING", "LIGHT", False, comm_codes).data()],
        )

    def test_pin_packet(self):
        self.assertEqual(
            [30, 1, 4, 32],
            [ord(x) for x in PinPacket(bytes([1]), comm_codes, index=4).data()],
        )
        self.assertEqual(
            [20, 1, 32], [ord(x) for x in PinPacket(bytes([1]), comm_codes).data()]
        )


class TestReader(TestCase):
    def test_debug(self):
        master, slave = openpty()
        port_name = ttyname(slave)

        serial = Serial(port=port_name)
        reader = SerialReader(serial, comm_codes["READ"], comm_codes["INPUT_PINS"], True)
        reader.start()

        message = 'Testing Output'

        write(master, bytes([100]))
        write(master, bytes([len(message)]))
        for character in message:
            write(master, str.encode(character))
        write(master, bytes([50]))
        sleep(0.5)

        matches = input(f"Is the output ARDUINO: {message}")
        self.assertNotEqual(matches, 'NO')

    def test_error(self):
        master, slave = openpty()
        port_name = ttyname(slave)

        serial = Serial(port=port_name)
        reader = SerialReader(serial, comm_codes["READ"], comm_codes["INPUT_PINS"], True)
        reader.start()

        message = 'Testing Error'

        write(master, bytes([25]))
        write(master, bytes([len(message)]))
        for character in message:
            write(master, str.encode(character))
        write(master, bytes([50]))
        sleep(0.5)

        matches = input(f"Is the output ARDUINO ERROR: {message}")
        self.assertNotEqual(matches, 'NO')


class TestWriter(TestCase):
    def test_relay_packet(self):
        master, slave = openpty()
        port_name = ttyname(slave)

        serial = Serial(port=port_name)
        writer = SerialWriter(serial, comm_codes["WRITE"])

        rp = RelayPacket("CEILING", "FAN", False, comm_codes)
        writer.write_packet(rp)

        result = []
        for i in range(4):
            result.append(ord(read(master, 1)))

        self.assertEqual(1, result)