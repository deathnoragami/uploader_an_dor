import vk_api
import os
import string
import re
import traceback

from work_files.messagebox_q import CustomMessageBox
from vk_api import VkUpload
from config import Config
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal, QThread, pyqtSlot, QMetaObject, Qt


class VkPostAnime(QObject):
    def __init__(self, check_nolink=None, name=None, number=None, post_id=None, path_image=None, select_dub=None):
        token = Config().get_vk_token()
        self.vk_session = vk_api.VkApi(token=f'{token}')
        self.vk = self.vk_session.get_api()
        self.group_id = -int(os.getenv('ID_GROUP_ANIME'))
        self.post_id = post_id
        self.number_seria = number
        self.name_anime = name 
        self.check_nolink = check_nolink
        self.path_image = path_image
        self.select_dub = select_dub

    def search_post(self):
        post_id = None
        for i in range(10):
            posts = self.vk.wall.get(owner_id=self.group_id, count=70, offset=i*70)
            if not len(posts['items']): 
                return None
            for post in posts['items']:
                post_text = post['text'].split('\n')[0]
                clean_post_text = ''.join(char if char not in string.punctuation else ' ' for char in post_text).lower().replace("  ", " ")
                clean_name_anime = ''.join(char if char not in string.punctuation else ' ' for char in self.name_anime).lower().replace("  ", " ")
                if clean_name_anime in clean_post_text:
                    reply = QMessageBox.question(None, "Что-то нашел", f"Этот ли прошлый пост?\n{post_text}", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
                    if reply == QMessageBox.Yes:
                        post_id = post['id']
                        return post_id
                    if reply == QMessageBox.No:
                        continue
                    if reply == QMessageBox.Cancel:
                        return None
        if not post_id:
            return None
    
           
    def post_vk(self):
        from connect_firebase import Connect
        db = Connect()
        uid = Config().get_uid_program()
        user = db.find_user_uid(uid)
        ping_timmer = user.get('ping')
        db.close()
        
        try:
            if self.post_id:
                post = self.vk.wall.getById(posts=f"{self.group_id}_{self.post_id}")
                post_text = post[0]['text']
                first_line = post_text.split('\n')[0]
                match = re.search(r'(\d+)\s*серия', first_line)
                self.number_seria = self.number_seria.rsplit('.', 1)[0]
                if match:
                    new_first_line = re.sub(r'(\d+)\s*серия', f'{int(self.number_seria)} серия', first_line)
                    new_text = post_text.replace(first_line, new_first_line)
                    if not self.check_nolink:
                        try:
                            pattern = r"(?<=Роли озвучивали: ).*"
                            new_text = re.sub(pattern, self.select_dub, new_text)
                            pattern = r"(?<=Тайминг и сведение: ).*"
                            new_text = re.sub(pattern, str(ping_timmer), new_text)
                        except Exception as e:
                            QMessageBox.warning(None, "Ошибка!", "Возможно пост не имеет дабберов или таймера в посту\nПосмотрите внимательно и если их там нет, то поставьте чекбокс на 'Без ссылок'")
                upload = vk_api.VkUpload(self.vk_session)
                photo = upload.photo_wall(f'{self.path_image}')[0]
                post = self.vk.wall.post(owner_id=self.group_id,
                                        message=new_text,
                                        attachments=f'photo{photo["owner_id"]}_{photo["id"]}')
                self.vk.likes.add(owner_id=self.group_id, type='post', item_id=post['post_id'])
                return True
        except Exception as e:
            traceback.print_exc()
            return False
                    
                             
