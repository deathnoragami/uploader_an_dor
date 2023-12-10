import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("timming-e844f-firebase-adminsdk-s0m6j-53a96d672b.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://timming-e844f-default-rtdb.europe-west1.firebasedatabase.app'})
user_ref = db.reference('Users')
user_data = user_ref.get()
dub_ref = db.reference('Dubbers')
dub_data = dub_ref.get()