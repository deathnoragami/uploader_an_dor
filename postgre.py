import psycopg2
import os

class Connect():
    def __init__(self):
        host = os.getenv('DB_HOST')
        database = os.getenv('DB_NAME')
        user = os.getenv('DB_NAME')
        password = os.getenv('DB_PASS')
        self.connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        self.cursor = self.connection.cursor()
                
    def get_user_data(self):
        self.cursor.execute("SELECT * FROM Users")
        user_data = self.cursor.fetchall()
        self.cursor.close()
        self.connection.close()
        return user_data
    
    def get_dub_data(self):
        self.cursor.execute("SELECT * FROM Dubbers")
        dub_data = self.cursor.fetchall()
        self.cursor.close()
        self.connection.close()
        return dub_data
    
    def find_user_uid(self, uid):
        self.cursor.execute("SELECT * FROM Users WHERE uid = %s", (uid,))
        user_data = self.cursor.fetchone()
        self.cursor.close()
        self.connection.close()
        return user_data
