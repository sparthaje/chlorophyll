# Shreepa Parthaje

import signal

from comms import Comms
from configs import SETTINGS, COMM_CODES
from firebase import Database


class Chloroplast:

    def __init__(self, settings, baudrate, comm_codes, firebase_secret, database_url):
        self.comms = Comms(settings, baudrate, comm_codes)
        self.database = Database(firebase_secret, database_url, self.comms.state_change)


def configure():
    return Chloroplast(SETTINGS['ENVIRONMENT'], SETTINGS['BAUDRATE'], COMM_CODES, SETTINGS['FIREBASE_SECRET'],
                       SETTINGS['DATABASE_ENDPOINT'])


if __name__ == '__main__':
    chloroplast = configure()
    signal.signal(signal.SIGINT, lambda sig, frame: chloroplast.comms.shutdown())
