// Shreepa Parthaje

#define BAUDRATE 9600

// Write Comm Codes
#define DEBUG_HEADER 0x64
#define FOOTER 0x32

// Read Comm COdes

void log(String message) {
    Serial.write(DEBUG_HEADER);
    Serial.write(byte(message.length()));
    Serial.print(message);
    Serial.write(FOOTER);
}

void setup() {
  Serial.begin(BAUDRATE);
  Serial.flush();
}

void loop() {
    if (Serial.available() > 0) {
        int incomingByte = Serial.read();
        if (incomingByte == 64) {
          log("header");
        }
        Serial.print(incomingByte);
    }
    // log("hello");
    delay(500);
}
