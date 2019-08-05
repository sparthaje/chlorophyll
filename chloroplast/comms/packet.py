# Shreepa Parthaje


class Packet:

    def __init__(self, location, fixture, value, comm_codes):
        self.location = location
        self.fixture = fixture
        self.value = value
        self.comm_codes = comm_codes

    def __str__(self):
        return f"Packet to set {self.fixture} at {self.location} to {'on' if self.value else 'off'}"

    def data(self):
        result = [self.comm_codes['WRITE']['PACKET_HEADER'],
                  self.comm_codes['NAME_MAP']['LOCATIONS'][self.location],
                  self.comm_codes['NAME_MAP']['FIXTURES'][self.fixture],
                  bytes([1]) if self.value else bytes([0]),
                  self.comm_codes['WRITE']['PACKET_FOOTER']]
        return result
