# Shreepa Parthaje

from os import path
from os.path import join

ROOT_DIR = path.dirname(path.dirname(path.abspath(__file__)))

SETTINGS = {
    'ENVIRONMENT': {
        'PRODUCTION': False,
        'DEBUG': True
    },
    'BAUDRATE': 9600,
    'FIREBASE_SECRET': join(ROOT_DIR, 'firebase.secret'),
    'DATABASE_ENDPOINT': join(ROOT_DIR, 'databaseurl.secret'),
}

COMM_CODES = {
    'READ': {
        'DEBUG_HEADER': 100,
        'ERROR_HEADER': 25,
        'FOOTER': 50
    },
    'WRITE': {
        'PACKET_HEADER': bytes([23]),
        'WRITE_FOOTER': bytes([32]),
        'SERIAL_CLOSE': bytes([40])
    },
    'NAME_MAP': {
        'LOCATIONS': {
            'CEILING': bytes([0])
        },
        'FIXTURES': {
            'FAN': bytes([0]),
            'LIGHT': bytes([1])
        }
    },
}
