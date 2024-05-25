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

    def add_name_ad(self, name, episode, ads):
        self.cursor.execute("INSERT INTO serial (name, episode, ads) VALUES (%s, %s, %s)", (name, episode, ads))
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        return True

    def search_ad(self, name:str, episode:int) -> tuple:
        episode = str(episode - 1)
        self.cursor.execute("SELECT ads FROM serial WHERE name = %s AND episode = %s", (name, episode))
        user_data = self.cursor.fetchone()
        self.cursor.close()
        self.connection.close()
        return user_data

    def search_ad_without_number(self, name:str) -> tuple:
        self.cursor.execute(
            "SELECT name, episode, ads FROM serial WHERE name = %s ORDER BY episode DESC LIMIT 1", (name,))
        user_data = self.cursor.fetchone()
        self.cursor.close()
        self.connection.close()
        return user_data

    def get_all_serials(self):
        self.cursor.execute("SELECT DISTINCT name FROM serial")
        serial_data = self.cursor.fetchall()
        self.cursor.close()
        self.connection.close()
        return serial_data
