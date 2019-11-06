# Shreepa Parthaje

import argparse
import signal

from comms import Comms
from configs import SETTINGS, COMM_CODES
from firebase import Database


class ArduinoChloroplast:
    def __init__(self, settings, baudrate, comm_codes, firebase_secret, database_url):
        self.comms = Comms(settings, baudrate, comm_codes)
        self.database = Database(
            firebase_secret,
            database_url,
            self.comms.set_pin_mode,
            self.comms.state_change,
        )
        self.comms.reader.handler = self.database.update_firebase


def set_env():
    parser = argparse.ArgumentParser(description="chloroplast env")
    parser.add_argument(
        "--production", help="Set production to True or False (default is True)"
    )
    parser.add_argument(
        "--debug", help="Set production to True or False (default is False)"
    )
    args = parser.parse_args()
    if args.debug:
        SETTINGS["ENVIRONMENT"]["DEBUG"] = args.debug == "True"
    if args.production:
        SETTINGS["ENVIRONMENT"]["PRODUCTION"] = args.production == "True"


def configure():
    set_env()
    return ArduinoChloroplast(
        SETTINGS["ENVIRONMENT"],
        SETTINGS["BAUDRATE"],
        COMM_CODES,
        SETTINGS["FIREBASE_SECRET"],
        SETTINGS["DATABASE_ENDPOINT"],
    )


if __name__ == "__main__":
    chloroplast = configure()
    signal.signal(signal.SIGINT, lambda sig, frame: chloroplast.comms.shutdown())
