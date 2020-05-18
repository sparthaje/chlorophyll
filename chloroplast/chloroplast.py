# Shreepa Parthaje

from configs import SETTINGS, PIN_MAP
from firebase import Database
from raspberrypi import Pi


def start_chloroplast():
    pi = Pi(PIN_MAP)
    database = Database(
        SETTINGS["FIREBASE_SECRET"],
        SETTINGS["DATABASE_ENDPOINT"],
        pi.update_relay,
    )
    pi.start()


if __name__ == "__main__":
    start_chloroplast()
