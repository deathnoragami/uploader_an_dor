import sqlite3
import os

class DataBase:
    def __init__(self):
        self.db_file = "assets/data.db"
        self.conn = sqlite3.connect(self.db_file)
        if os.path.exists("assets/data.db"):
            self.create_empty_database()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

    def create_empty_database(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS anime (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path_pic TEXT,
                path_video TEXT,
                folder_sftp TEXT,
                check_sftp INTEGER,
                check_malf INTEGER,
                check_nolink INTEGER,
                check_post_site INTEGER,
                link_site TEXT,
                link_second_site TEXT,
                vk_post_id INTEGER
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dorama (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path_video TEXT,
                path_pic TEXT,
                folder_sftp TEXT,
                check_sftp INTEGER,
                check_vk INTEGER,
                check_telegram INTEGER,
                check_site INTEGER,
                check_novideo_vk INTEGER,
                vk_post_id INTEGER,
                vk_playlist_id INTEGER,
                tg_post_id INTEGER,
                link_site TEXT,
                link_second_site TEXT
            )
        """)
        # добавить колонку
        # cursor.execute("PRAGMA table_info(anime)")
        # columns = cursor.fetchall()
        # existing_columns = [column[1] for column in columns]
        
        # if "video" not in existing_columns:
        #     cursor.execute(f"ALTER TABLE anime ADD COLUMN video INTEGER")
        # else:
        #     print(f"Column 'video' already exists in the table.")

    def add_dorama(self, path_video, path_pic, folder_sftp, 
                   check_sftp, check_vk, check_telegram, 
                   check_site, check_novideo_vk, vk_post_id, vk_playlist_id, 
                   tg_post_id, link_site, link_second_site):
        cursor = self.conn.cursor()
        cursor.execute(f"""
            INSERT INTO dorama (
                path_video, path_pic, folder_sftp,
                check_sftp, check_vk, check_telegram,
                check_site, check_novideo_vk, vk_post_id, vk_playlist_id,
                tg_post_id, link_site, link_second_site
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            path_video, path_pic, folder_sftp,
            check_sftp, check_vk, check_telegram,
            check_site, check_novideo_vk, vk_post_id, vk_playlist_id,
            tg_post_id, link_site, link_second_site
        ))
        self.conn.commit()

    def update_dorama(self, path_video, update_values):
        cursor = self.conn.cursor()
        # Порядок ключей
        keys_order = [
            "path_pic",
            "check_sftp",
            "check_vk",
            "check_telegram",
            "check_site",
            "check_novideo_vk",
            "link_site",
            "link_second_site",
            "folder_sftp",
            "vk_post_id",
            "vk_playlist_id",
            "tg_post_id"
        ]

        # Создаем список значений и часть запроса SET с сохранением порядка ключей
        values_to_update = []
        set_clause_parts = []
        for key in keys_order:
            value = update_values.get(key, None)
            if value is not None:
                values_to_update.append(value)
                set_clause_parts.append(f"{key} = ?")

        # Генерируем часть запроса SET
        set_clause = ", ".join(set_clause_parts)
        values_to_update.append(path_video)
        cursor.execute(f"""
            UPDATE dorama 
            SET {set_clause}
            WHERE path_video = ?
        """, values_to_update)
        self.conn.commit()

    def add_anime(self, path_pic, path_video, 
                  folder_sftp, check_sftp, check_malf, 
                  check_nolink, check_post_site, link_site, 
                  vk_post_id, link_second_site=None):
        cursor = self.conn.cursor()
        cursor.execute(f"""
            INSERT INTO anime (
                path_pic, path_video, folder_sftp,
                check_sftp, check_malf, check_nolink,
                check_post_site, link_site, link_second_site,
                vk_post_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            path_pic, path_video, folder_sftp,
            check_sftp, check_malf, check_nolink,
            check_post_site, link_site, link_second_site, vk_post_id
        ))
        self.conn.commit()

    def update_anime(self, path_pic, path_video, 
                  folder_sftp, check_sftp, check_malf, 
                  check_nolink, check_post_site, link_site, 
                  link_second_site=None):
        cursor = self.conn.cursor()
        cursor.execute(f"""
            UPDATE anime 
            SET path_video = ?, folder_sftp = ?,
                check_sftp = ?, check_malf = ?, check_nolink = ?,
                check_post_site = ?, link_site = ?, link_second_site = ?
            WHERE path_pic = ?
        """, (path_video, folder_sftp, check_sftp,
              check_malf, check_nolink, check_post_site,
              link_site, link_second_site, path_pic))
        self.conn.commit()

    def search_by_path_pic_anime(self, path_pic):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM anime WHERE path_pic=?", (path_pic,))
        result = cursor.fetchall()
        return result
    
    def search_by_path_video_dor(self, path_video):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM dorama WHERE path_video=?", (path_video,))
        result = cursor.fetchall()
        return result

    