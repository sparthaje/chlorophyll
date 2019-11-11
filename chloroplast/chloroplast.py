# Shreepa Parthaje

import argparse
import signal

from comms import Comms
from configs import SETTINGS, COMM_CODES, PIN_MAP
from firebase import Database
from raspberrypi import Pi


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

    def shutdown(self):
        self.comms.shutdown()


class RaspberryPiChloroplast:
    def __init__(self, settings, pin_map, firebase_secret, database_url):
        self.pi = Pi(settings, pin_map)
        self.database = Database(
            firebase_secret,
            database_url,
            lambda: 1,
            self.pi.state_change,
        )
        self.pi.reader.handler = self.database.update_firebase

    def shutdown(self):
        return


def set_env():
    parser = argparse.ArgumentParser(description="chloroplast env")
    parser.add_argument(
        "--production", help="Set production to True or False (default is True)"
    )
    parser.add_argument(
        "--arduino", help="Use a connected arduino instead of RaspberryPi GPIO pins"
    )
    parser.add_argument(
        "--debug", help="Set production to True or False (default is False)"
    )
    args = parser.parse_args()
    if args.debug:
        SETTINGS["ENVIRONMENT"]["DEBUG"] = args.debug == "True"
    if args.production:
        SETTINGS["ENVIRONMENT"]["PRODUCTION"] = args.production == "True"
    if args.arduino:
        SETTINGS["ENVIRONMENT"]["USES_ARDUINO"] = args.arduino == "True"


def configure():
    set_env()
    if SETTINGS["ENVIRONMENT"]["USES_ARDUINO"]:
        return ArduinoChloroplast(
            SETTINGS["ENVIRONMENT"],
            SETTINGS["BAUDRATE"],
            COMM_CODES,
            SETTINGS["FIREBASE_SECRET"],
            SETTINGS["DATABASE_ENDPOINT"],
        )
    return RaspberryPiChloroplast(
        SETTINGS["ENVIRONMENT"],
        PIN_MAP,
        SETTINGS["FIREBASE_SECRET"],
        SETTINGS["DATABASE_ENDPOINT"],
    )


if __name__ == "__main__":
    chloroplast = configure()
    signal.signal(signal.SIGINT, lambda sig, frame: chloroplast.shutdown())
