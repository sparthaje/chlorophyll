# Shreepa Parthaje

from time import sleep

import firebase_admin
from firebase_admin import db, credentials


class Database:
    @staticmethod
    def update_firebase(location, fixture):
        db_reference = db.reference("/state").child(location).child(fixture)
        db_reference.set(not db_reference.get())

    def handle_firebase_update(self, event):
        """ Handles a change in the firebase realtime database """

        path = event.path
        data = event.data

        if isinstance(data, bool):
            self.handler(path, data)

    def configure_current_state(self, state):
        """ Configures the current state in the database on run """

        sleep(2)
        self.set_pin_modes()

        current = state.get()
        for location in current:
            for fixture in current[location]:
                self.handler(f"/{location}/{fixture}", current[location][fixture])

    def configure_firebase(self, firebase_secret, database_url):
        """ Handles the security while connecting the firebase_update method to updates in the database """

        cred = credentials.Certificate(firebase_secret)
        with open(database_url) as f:
            firebase_admin.initialize_app(cred, {"databaseURL": f.read()})
        state = db.reference("/state")

        self.configure_current_state(state)
        state.listen(self.handle_firebase_update)

    def __init__(self, firebase_secret, database_url, set_pin_modes, handler):
        """ Takes the filenames for the secret information and two methods to handle
            setting pin modes and setting the relays based on firebase changes """
        self.set_pin_modes = set_pin_modes
        self.handler = handler
        self.configure_firebase(firebase_secret, database_url)
