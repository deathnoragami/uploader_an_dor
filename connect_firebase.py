import firebase_admin
from firebase_admin import credentials, firestore

import os

class Connect():
    def __init__(self):
        cred = credentials.Certificate("timming-e844f-firebase-adminsdk-s0m6j-53a96d672b.json")
        # self.app = firebase_admin.initialize_app(cred, {'databaseURL': f'{os.getenv("DB_URL")}'})
        self.app = firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        
        
    def get_user_data(self):
        user_ref = self.db('Users')
        user_data = user_ref.get()
        return user_data
    
    def get_dub_data(self):
        user_ref = self.db.collection("Dubbers")
        user_data = [{'id': doc.id, **doc.to_dict()} for doc in user_ref.stream()]
        return user_data
    
    def close(self):
        firebase_admin.delete_app(self.app)
    
if __name__ == "__main__":
    Connect()
