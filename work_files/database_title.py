import json
import os


class DatabaseManager:
    def __init__(self):
        self.db_file = 'assets/title.json'
        self.load_database()
        
        
    def load_database(self):
        if not os.path.exists(self.db_file):
            self.create_empty_database()
        try:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                self.database = json.load(f)
        except FileNotFoundError:
            print("Ошибка загрузки локальной БД.")
            
            
    def save_database(self):
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.database, f, indent=4, ensure_ascii=False)
            
    
    def create_empty_database(self):
        self.database = {"anime": [], "dorama": []}
        self.save_database()
    
    
    def add_entry(self, 
                  path_pic, 
                  path_video, 
                  folder_sftp, 
                  check_sftp, 
                  check_malf, 
                  check_nolink,
                  check_post_site,
                  link_site, 
                  vk_post_id, 
                  chosen, 
                  link_second_site=None): #TODO: айди поста
        if chosen == 'anime':
            entry = {
                "path_pic": path_pic,
                "path_video": path_video,
                "folder_sftp": folder_sftp,
                "check_sftp": check_sftp,
                "check_malf": check_malf,
                "check_nolink": check_nolink,
                "check_post_site": check_post_site,
                "link_site": link_site,
                "link_second_site": link_second_site,
                "vk_post_id": vk_post_id}
            self.database["anime"].append(entry)
            self.save_database()
        elif chosen == 'dorama':
            entry = {
                "path_pic": path_pic,
                "path_video": path_video,
                "folder_sftp": folder_sftp,
                "check_sftp": check_sftp,
                "check_vk": check_malf,
                "check_telegram": check_nolink,
                "link_site": link_site,
                "link_second_site": link_second_site,}
            self.database["dorama"].append(entry)
            self.save_database()
            
    def update_data(self, path_pic, chosen, 
                  path_video = None, 
                  folder_sftp = None, 
                  check_sftp = None, 
                  check_malf = None, 
                  check_nolink = None,
                  check_post_site = None,
                  link_site = None, 
                  vk_post_id = None, 
                  link_second_site=None):
        if chosen == 'anime':
            for entry in  self.database['anime']:
                if entry["path_pic"] == path_pic:
                    if path_video and path_video !=  entry["path_video"]:
                        entry["path_video"] = path_video
        
        
    def search_by_path_pic_anime(self, path_pic):
        result = [entry for entry in self.database["anime"] if entry["path_pic"] == path_pic]
        return result
    

    def search_by_path_video_dorama(self, path_video):
        result = [entry for entry in self.database["dorama"] if entry["path_video"] == path_video]
        return result
    
    