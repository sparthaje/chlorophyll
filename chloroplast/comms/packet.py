# Shreepa Parthaje


class Packet:

    def __init__(self, location, fixture, value):
        self.location = location
        self.fixture = fixture
        self.value = value

    def __str__(self):
        return f"Packet to set {self.fixture} at {self.location} to {'on' if self.value else 'off'}"
