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
        user_ref = self.db.collection("Users")
        user_data = user_ref.get()
        return user_data.to_dict()
    
    def get_dub_data(self):
        user_ref = self.db.collection("Dubbers")
        user_data = [{'id': doc.id, **doc.to_dict()} for doc in user_ref.stream()]
        return user_data
    
    def find_user_uid(self, uid):
        user_ref = self.db.collection("Users")
        user_data = user_ref.where('uid', '==', uid).limit(1).get()
        if user_data:
            user_data = user_data[0].to_dict()
            return user_data
        
        return None
    
    def update_malf_data(self, uid, login, password):
        user_ref = self.db.collection("Users")
        user_data = user_ref.where('uid', '==', uid).limit(1).get()
        if user_data:
            user_data = user_data[0]
            user_ref.document(user_data.id).update({
                'malf_login': login,
                'malf_pass': password,
            })
            
    def update_maunt_data(self, uid, login, password):
        user_ref = self.db.collection("Users")
        user_data = user_ref.where('uid', '==', uid).limit(1).get()
        if user_data:
            user_data = user_data[0]
            user_ref.document(user_data.id).update({
                'maunt_login': login,
                'maunt_pass': password,
            })
    
    def close(self):
        firebase_admin.delete_app(self.app)
    
if __name__ == "__main__":
    Connect()
