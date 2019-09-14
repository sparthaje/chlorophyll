// Shreepa Parthaje

const int BAUDRATE = 9600;

// Write Comm Codes
const byte DEBUG_HEADER = 0x64;
const byte ERROR_HEADER = 0x19;
const byte STATE_HEADER = 0x25;
const byte WRITE_FOOTER = 0x32;

// Read Comm Codes
const int PACKET_HEADER = 23;
const int OUTPUT_HEADER = 20;
const int INPUT_HEADER = 30;
const int READ_FOOTER = 32;
const int SERIAL_CLOSE = 40;

// Inputs
const int inputs = 2;
int inputPins[inputs] = {0, 0};
int inputStates[inputs] = {0, 0};

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

void writeInput(int pin) {
    Serial.write(STATE_HEADER);
    Serial.write(byte(pin));
    Serial.write(WRITE_FOOTER);
}

void readPacket() {
    int pinNumber = Serial.read();
    int value = Serial.read();

    String v = "ON";
    if (value == 0) {
        v = "OFF";
    }

    if (int(Serial.read()) != READ_FOOTER) {
        error("Packet data is corrupted. Should be [32, pinNumber, value, 23]");
        return;
    }

    digitalWrite(pinNumber, value);
    log(String(pinNumber) + "/" + v);
}

void indicateSerialClose() {
    for (int i = 0; i < 15; i++) {
        digitalWrite(13, 1);
        delay(50);
        digitalWrite(13, 0);
        delay(50);
    }
}

void setPin(bool output) {
    int pinNumber = Serial.read();

    if (!output) {
        int index = Serial.read();
        inputPins[index] = pinNumber;
    }

    if (int(Serial.read()) != READ_FOOTER) {
        if (output) {
            error("Output packet data is corrupted. Should be [20, pinNumber, 23]");
        }
        error("Input packet data is corrupted. Should be [30, pinNumber, 23]");
        return;
    }

    if (output) {
        pinMode(pinNumber, OUTPUT);
        return;
    }

    pinMode(pinNumber, INPUT);
}

void readData() {
    if (Serial.available() > 0) {
        int header = Serial.read();
        switch (header) {
            case PACKET_HEADER:
                readPacket();
                break;
            case OUTPUT_HEADER:
                setPin(true);
                break;
            case INPUT_HEADER:
                setPin(false);
                break;
            case SERIAL_CLOSE:
                indicateSerialClose();
                break;
            default:
                break;
        }
    }
}

void readInput() {
    for (int index = 0; index < inputs; index ++) {
        int pin = inputPins[index];
        int currentState = inputStates[index];
        int reading = digitalRead(pin);

        if (reading != currentState) {
            if (reading == 1) {
                // First time the button is clicked
                inputStates[index] = 1;
                writeInput(pin);
                log(String(pin) + " has been clicked");
            } else {
                // Button has been let go
                inputStates[index] = 0;
            }
        }
    }
}

void setup() {
    // Start serial
    Serial.begin(BAUDRATE);
    Serial.flush();

    // Turn built-in LED to output
    pinMode(13, OUTPUT);
}

void loop() {
    readData();
    readInput();
    delay(100);
}
