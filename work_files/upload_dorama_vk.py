import vk_api
from config import Config
import os
import string
from PyQt5.QtWidgets import QMessageBox



class UploadDoramaVK():
   
    def __init__(self):
        token = Config().get_vk_token()
        vk_session = vk_api.VkApi(token=f'{token}')
        self.vk = vk_session.get_api()
        self.group_id = -int(os.getenv("ID_GROUP_DORAMA"))
    
    def search_vk_dorama(self, file_path):
        playlist_name = os.path.basename(os.path.dirname(file_path))
        playlist_name = ''.join(char if char not in string.punctuation else ' ' for char in playlist_name).lower().replace("  ", " ")
        playlist_id = None
        for i in range(10):
            if playlist_id:
                break
            playlists = self.vk.video.getAlbums(owner_id=self.group_id, count=70, offset=i*70+1)
            for playlist in playlists['items']:
                playlist_vk = ''.join(char if char not in string.punctuation else ' ' for char in playlist['title']).lower().replace("  ", " ")
                if playlist_name in playlist_vk:
                    q = QMessageBox.question(None, "Что-то нашел", f"Нашел плейлист, его название верно?\n{playlist['title']}", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
                    if q == QMessageBox.Yes:
                        playlist_id = playlist['id']
                        break
                    elif q == QMessageBox.No:
                        continue
                    else:
                        return None
        if not playlist_id:
            QMessageBox.information(None, "Информация", "Ничего не нашел")
            return None
        post_id = None
        for i in range(10):
            posts = self.vk.wall.get(owner_id=self.group_id, count=70, offset=i*70+1)
            if not len(posts['items']):
                return None
            for post in posts['items']:
                post_text = post['text'].split('\n')[0]
                clean_post_text = ''.join(char if char not in string.punctuation else ' ' for char in post_text).lower().replace("  ", " ")
                if playlist_name in clean_post_text:
                    q = QMessageBox.question(None, "Что-то нашел", f"Этот ли прошлый пост?\n{post_text}", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
                    if q == QMessageBox.Yes:
                        return post['id'], playlist_id
                    elif q == QMessageBox.No:
                        continue
                    else:
                        return None
        if not post_id:
            QMessageBox.warning(None, "Ошибка", "Не найден нужный пост, смените название папки для более точного названия, либо пост был сделан более 2-3 месяцев назад.")
            return None
        
        