import getpass
from os import makedirs
from os.path import join, exists
from time import sleep

import firebase_admin
from firebase_admin import db, credentials
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

cred = credentials.Certificate('firebase.secret')
path = f'/home/{getpass.getuser()}/.config/chloroplast'

if not exists(path):
    makedirs(path)

for file in [join(path, f) for f in ['light', 'fan']]:
    if not exists(file):
        with open(file, 'w') as f:
            f.write('welcome')

with open('databaseurl.secret') as f:
    firebase_admin.initialize_app(cred, {
        'databaseURL': f.read()
    })
state = db.reference('/state')


class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        if 'light' in event.src_path:
            db_reference = db.reference('/state').child('CEILING').child('LIGHT')
            db_reference.set(not db_reference.get())
        elif 'fan' in event.src_path:
            db_reference = db.reference('/state').child('CEILING').child('FAN')
            db_reference.set(not db_reference.get())


observer = Observer()
observer.schedule(Handler(), join(path, ''))
observer.start()
try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    observer.stop()
    observer.join()
