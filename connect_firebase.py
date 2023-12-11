import firebase_admin
from firebase_admin import credentials, db


class Connect():
    def __init__(self):
        cred = credentials.Certificate("timming-e844f-firebase-adminsdk-s0m6j-53a96d672b.json")
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://timming-e844f-default-rtdb.europe-west1.firebasedatabase.app'})
        
    def get_user_data(self):
        user_ref = db.reference('Users')
        user_data = user_ref.get()
        return user_data
    
    def get_dub_data(self):
        dub_ref = db.reference('Dubbers')
        dub_data = dub_ref.get()
        return dub_data