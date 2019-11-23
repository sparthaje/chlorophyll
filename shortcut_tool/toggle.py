from sys import argv
import firebase_admin
from firebase_admin import db, credentials

loc = argv[1]
item = argv[2]

cred = credentials.Certificate('firebase.secret')
with open('databaseurl.secret') as f:
    firebase_admin.initialize_app(cred, {
        'databaseURL': f.read()
    })
state = db.reference('/state')
db_reference = db.reference('/state').child(loc).child(item)
db_reference.set(not db_reference.get())
