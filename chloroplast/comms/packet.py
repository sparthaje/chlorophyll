# Shreepa Parthaje


class RelayPacket:

    def __init__(self, location, fixture, value, comm_codes):
        self.location = location
        self.fixture = fixture
        self.value = value
        self.comm_codes = comm_codes

    def __str__(self):
        return f"Packet to set {self.fixture} at {self.location} to {'on' if self.value else 'off'}"

    def data(self):
        return [self.comm_codes['WRITE']['PACKET_HEADER'],
                self.comm_codes['OUTPUT_PINS'][self.location][self.fixture],
                bytes([1]) if self.value else bytes([0]),
                self.comm_codes['WRITE']['WRITE_FOOTER']]


class PinPacket:

    def __init__(self, output, pin_number_bytes, comm_codes):
        self.output = output
        self.pin_number_bytes = pin_number_bytes
        self.comm_codes = comm_codes

    def __str__(self):
        return f"Packet to set pin {int.from_bytes(self.pin_number_bytes, byteorder='big')} to {'output' if self.output else 'input'} "

    def data(self):
        return [self.comm_codes['WRITE']['OUTPUT_HEADER'] if self.output else self.comm_codes['WRITE']['INPUT_HEADER'],
                self.pin_number_bytes,
                self.comm_codes['WRITE']['WRITE_FOOTER']]
