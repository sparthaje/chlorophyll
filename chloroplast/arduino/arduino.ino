// Shreepa Parthaje

const int BAUDRATE = 9600;

// Write Comm Codes
const byte DEBUG_HEADER = 0x64;
const byte ERROR_HEADER = 0x19;
const byte WRITE_FOOTER = 0x32;

// Read Comm Codes
const int PACKET_HEADER = 23;
const int READ_FOOTER = 32;

// Ceiling Relay Pins
const int ceilingFixtures = 2;
const int ceilingFixturePins[] = {2, 13};

void log(String message) {
    Serial.write(DEBUG_HEADER);
    Serial.write(byte(message.length()));
    Serial.print(message);
    Serial.write(WRITE_FOOTER);
}

void error(String message) {
    Serial.write(ERROR_HEADER);
    Serial.write(byte(message.length()));
    Serial.print(message);
    Serial.write(WRITE_FOOTER);
}

void changeCeilingState(int fixture, int value) {
    if (fixture + 1 > ceilingFixtures) {
        error("Invalid fixture value");
        return;
    }

    if (value > 1) {
        error("Invalid state (either 0 or 1)");
        return;
    }

    digitalWrite(ceilingFixturePins[fixture], value);
}

void readPacket() {
    int location = Serial.read();
    int fixture = Serial.read();
    int value = Serial.read();

    if (int(Serial.read()) != READ_FOOTER) {
        error("Packet data is corrupted. Should be [32, location, fixture, value, 23]");
    } else {
        log("Location is " + String(location) + "; Fixture is " + String(fixture) + "; Value is " + String(value));
        switch (location) {
            case 0:
                changeCeilingState(fixture, value);
                break;
            default:
                error("Unknown location");
                break;
        }
    }
}

void readData() {
    if (Serial.available() > 0) {
        int header = Serial.read();
        switch (header) {
            case PACKET_HEADER:
                readPacket();
                break;
            default:
                break;
        }
    }
}

void setup() {
    Serial.begin(BAUDRATE);
    Serial.flush();

    for (int i = 0; i < ceilingFixtures; i++) {
        pinMode(ceilingFixturePins[i], OUTPUT);
    }

}

void loop() {
    readData();
    delay(100);
}
