// Shreepa Parthaje

#define BAUDRATE 9600

// Write Comm Codes
#define DEBUG_HEADER 0x64
#define WRITE_FOOTER 0x32

// Read Comm Codes
#define PACKET_HEADER 23
#define READ_FOOTER 32

void log(String message) {
    Serial.write(DEBUG_HEADER);
    Serial.write(byte(message.length()));
    Serial.print(message);
    Serial.write(WRITE_FOOTER);
}

void setup() {
  Serial.begin(BAUDRATE);
  Serial.flush();
}

void loop() {
    if (Serial.available() > 0) {
        int next = Serial.read();

        if (next == PACKET_HEADER) {
          int location = Serial.read();
          int fixture = Serial.read();
          int value = Serial.read();

          if (int(Serial.read()) != READ_FOOTER) {
            log("Corrupted data, should be header, three ints, footer");
          } else {
            // write diff methods based on location value
            log("Location is " + String(location) + "; Fixture is " + String(fixture) + "; Value is " + String(value));
          }
        }
    }
    delay(100);
}
