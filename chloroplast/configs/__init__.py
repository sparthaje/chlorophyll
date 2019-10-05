# Shreepa Parthaje

from os import path
from os.path import join

ROOT_DIR = path.dirname(path.dirname(path.abspath(__file__)))

SETTINGS = {
    "ENVIRONMENT": {"PRODUCTION": True, "DEBUG": False},
    "BAUDRATE": 9600,
    "FIREBASE_SECRET": join(ROOT_DIR, "firebase.secret"),
    "DATABASE_ENDPOINT": join(ROOT_DIR, "databaseurl.secret"),
}

COMM_CODES = {
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
