# Shreepa Parthaje

from os import path
from os.path import join

ROOT_DIR = path.dirname(path.dirname(path.abspath(__file__)))

SETTINGS = {
    "ENVIRONMENT": {
        "PRODUCTION": True,
        "DEBUG": True,
    },
    "FIREBASE_SECRET": join(ROOT_DIR, "firebase.secret"),
    "DATABASE_ENDPOINT": join(ROOT_DIR, "databaseurl.secret"),
}

PIN_MAP = {
    "OUTPUT": {
        "CEILING": {
            "FAN": 8,
            "LIGHT": 10
        }
    },
    "INPUT": {
        "CEILING": {
            "FAN": 7,
            "LIGHT": 11
        }
    },
}
