# Shreepa Parthaje

import firebase_admin
from firebase_admin import db, credentials

from comms.communication import state_change, set_serial
from comms.arduino import get_serial_ports


def firebase_update(event):
    path = event.path
    data = event.data

    if isinstance(data, bool):
        state_change(path, data)


def configure_firebase():
    cred = credentials.Certificate('firebase.secret')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://chlorophyll-11474.firebaseio.com/'
    })
    state = db.reference('/state')
    state.listen(firebase_update)


def configure_arduino():
    ports = get_serial_ports()

    if len(ports) == 0:
        raise OSError("no serial device connected")

    if len(ports) == 1:
        port_index = 0
    else:
        port_index = int(input(f"Choose which serial port to use: {ports}: "))

    set_serial(ports[port_index])


def configure():
    configure_firebase()
    # configure_arduino()


if __name__ == '__main__':
    configure()
    port = input()
