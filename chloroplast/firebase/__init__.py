# Shreepa Parthaje

from time import sleep

import firebase_admin
from firebase_admin import db, credentials


class Database:

    def handle_firebase_update(self, event):
        """ Handles a change in the firebase realtime database """

        path = event.path
        data = event.data

        if isinstance(data, bool):
            self.handler(path, data)

    def __init__(self, firebase_secret, database_url, handler):
        """ Takes the filenames for the secret information and two methods to handle
            setting pin modes and setting the relays based on firebase changes """
        self.handler = handler

        cred = credentials.Certificate(firebase_secret)
        with open(database_url) as f:
            firebase_admin.initialize_app(cred, {"databaseURL": f.read()})

        state = db.reference("/state")

        sleep(2)

        current = state.get()
        for location in current:
            for fixture in current[location]:
                self.handler(f"/{location}/{fixture}", current[location][fixture])

        state.listen(self.handle_firebase_update)
