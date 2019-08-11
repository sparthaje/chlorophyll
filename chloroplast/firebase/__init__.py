# Shreepa Parthaje

from time import sleep

import firebase_admin
from firebase_admin import db, credentials


class Database:

    def firebase_update(self, event):
        path = event.path
        data = event.data

        if isinstance(data, bool):
            self.handler(path, data)

    def configure_current_state(self, state):
        sleep(2)
        current = state.get()
        for location in current:
            for fixture in current[location]:
                self.handler(f'/{location}/{fixture}', current[location][fixture])

    def configure_firebase(self, firebase_secret, database_url):
        cred = credentials.Certificate(firebase_secret)
        with open(database_url) as f:
            firebase_admin.initialize_app(cred, {
                'databaseURL': f.read()
            })
        state = db.reference('/state')

        self.configure_current_state(state)
        state.listen(self.firebase_update)

    def __init__(self, firebase_secret, database_url, handler):
        self.handler = handler
        self.configure_firebase(firebase_secret, database_url)
