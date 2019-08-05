# Shreepa Parthaje

SETTINGS = {
    'ENVIRONMENT': {
        'PRODUCTION': False,
        'DEBUG': True
    },
    'BAUDRATE': 9600,
    'FIREBASE_SECRET': 'firebase.secret',
    'DATABASE_ENDPOINT': 'databaseurl.secret',
}

COMM_CODES = {
    'READ': {
        'DEBUG_HEADER': 100,
        'ERROR_HEADER': 25,
        'FOOTER': 50
    },
    'WRITE': {
        'PACKET_HEADER': bytes([23]),
        'PACKET_FOOTER': bytes([32])
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
