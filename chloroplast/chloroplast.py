# Shreepa Parthaje

import firebase_admin
from firebase_admin import db, credentials

from comms.communication import Comms


class Chloroplast:
    def firebase_update(self, event):
        path = event.path
        data = event.data

        if isinstance(data, bool):
            self.comms.state_change(path, data)

    def configure_firebase(self, firebase_secret, database_url):
        cred = credentials.Certificate(firebase_secret)
        with open(database_url) as f:
            firebase_admin.initialize_app(cred, {
                'databaseURL': f.read()
            })
        state = db.reference('/state')
        state.listen(self.firebase_update)

    def __init__(self, firebase_secret, database_url):
        self.comms = Comms()
        self.configure_firebase(firebase_secret, database_url)


def configure():
    return Chloroplast('firebase.secret', 'databaseurl.secret')


if __name__ == '__main__':
    chloroplast = configure()
