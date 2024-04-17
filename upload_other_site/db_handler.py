import sqlite3


class DatabaseHandler:
    def __init__(self):
        self.db_file = "./assets/upload_other_site.db"
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS data (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    animaunt_link TEXT,
                    find_link TEXT,
                    _365_link TEXT,
                    path TEXT
                )
            ''')
            conn.commit()

    def insert_data(self, name, animaunt_link, find_link, _365_link, path):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO data (name, animaunt_link, find_link, _365_link, path)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, animaunt_link, find_link, _365_link, path))
            conn.commit()

    def get_data_by_name(self, name):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM data WHERE name = ?
            ''', (name,))
            row = cursor.fetchone()
            return row if row else None


if __name__ == '__main__':
    pass
