# Shreepa Parthaje


class RelayPacket:
    """ RelayPacket transforms str data from the database into a byte array to send via serial """

    def __init__(self, location, fixture, value, comm_codes):
        self.location = location
        self.fixture = fixture
        self.value = value
        self.comm_codes = comm_codes

    def __str__(self):
        return f"Packet to set {self.fixture} at {self.location} to {'on' if self.value else 'off'}"

    def data(self):
        return [
            self.comm_codes["WRITE"]["PACKET_HEADER"],
            self.comm_codes["OUTPUT_PINS"][self.location][self.fixture],
            bytes([1]) if self.value else bytes([0]),
            self.comm_codes["WRITE"]["WRITE_FOOTER"],
        ]


class PinPacket:
    """ PinPacket creates an array of bytes to configure a pin to output/input via serial """

    def __init__(self, pin_number_bytes, comm_codes, index=None):
        self.pin_number_bytes = pin_number_bytes
        self.comm_codes = comm_codes
        self.index = index

    def __str__(self):
        return f"Packet to set pin {int.from_bytes(self.pin_number_bytes, byteorder='big')} to {'output' if self.output else 'input'} "

    def data(self):
        if self.index is None:
            return [
                self.comm_codes["WRITE"]["OUTPUT_HEADER"],
                self.pin_number_bytes,
                self.comm_codes["WRITE"]["WRITE_FOOTER"],
            ]
        return [
            self.comm_codes["WRITE"]["INPUT_HEADER"],
            self.pin_number_bytes,
            bytes([self.index]),
            self.comm_codes["WRITE"]["WRITE_FOOTER"],
        ]
