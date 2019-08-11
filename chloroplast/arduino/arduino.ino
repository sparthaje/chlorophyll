// Shreepa Parthaje

const int BAUDRATE = 9600;

// Write Comm Codes
const byte DEBUG_HEADER = 0x64;
const byte ERROR_HEADER = 0x19;
const byte WRITE_FOOTER = 0x32;

// Read Comm Codes
const int PACKET_HEADER = 23;
const int READ_FOOTER = 32;
const int SERIAL_CLOSE = 40;

// Relay Pin Information
const int locations = 1;
const int maxPinsLocation = 5;

// Relay Pins Definition
const int fixturePins[locations][maxPinsLocation] = {
    {2, 13, 0, 0, 0} // Ceiling
};
const int fixturePinsLength[locations] = {
    2 // Ceiling
};

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

void changeState(int location, int fixture, int value) {
    if (fixture >= fixturePinsLength[location]) {
        error("Invalid fixture value: " + String(fixture));
        return;
    }

    if (value > 1) {
        error("Invalid state: " + String(value));
        return;
    }

    log(String(fixturePins[location][fixture])+ "/" + String(value) + " " +  String(location) + String(fixture) + String(value));
    digitalWrite(fixturePins[location][fixture], value);
}

void readPacket() {
    int location = Serial.read();
    int fixture = Serial.read();
    int value = Serial.read();

    if (int(Serial.read()) != READ_FOOTER) {
        error("Packet data is corrupted. Should be [32, location, fixture, value, 23]");
        return;
    }

    if (location >= locations) {
        error("Unknown location: " + String(location));
        return;
    }

    changeState(location, fixture, value);
}

void indicateSerialClose() {
    for (int i = 0; i < 15; i++) {
        digitalWrite(13, 1);
        delay(50);
        digitalWrite(13, 0);
        delay(50);
    }
}

void readData() {
    if (Serial.available() > 0) {
        int header = Serial.read();
        switch (header) {
            case PACKET_HEADER:
                readPacket();
                break;
            case SERIAL_CLOSE:
                indicateSerialClose();
                break;
            default:
                break;
        }
    }
}

void setup() {
    // Start serial
    Serial.begin(BAUDRATE);
    Serial.flush();

    // Turn built-in LED to output
    pinMode(13, OUTPUT);

    // Set all relay pins to output
    for (int location = 0; location < locations; location++) {
        for (int pin = 0; pin < fixturePinsLength[location]; pin++) {
            log("Setting pin " + String(fixturePins[location][pin]) + " at location " + String(location) + " to output.");
            pinMode(fixturePins[location][pin], OUTPUT);
        }
    }

}

void loop() {
    readData();
    delay(100);
}
