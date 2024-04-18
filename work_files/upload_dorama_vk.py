import vk_api
from vk_api import VkUpload
from config import Config
import os
import string
import re
import time
from PyQt5.QtWidgets import QMessageBox
from playwright.sync_api import sync_playwright
from postgre import Connect
import traceback
import log_config



class UploadDoramaVK():
    def __init__(self):
        token = Config().get_vk_token()
        self.vk_session = vk_api.VkApi(token=f'{token}')
        self.vk = self.vk_session.get_api()
        self.group_id = -int(os.getenv("ID_GROUP_DORAMA"))


    def search_vk_dorama(self, file_path):
        playlist_name = os.path.basename(os.path.dirname(file_path))
        playlist_name = ''.join(char if char not in string.punctuation else ' ' for char in playlist_name).lower().replace("  ", " ")
        playlist_id = None
        for i in range(10):
            if playlist_id:
                break
            playlists = self.vk.video.getAlbums(owner_id=self.group_id, count=70, offset=i*71)
            for playlist in playlists['items']:
                playlist_vk = ''.join(char if char not in string.punctuation else ' ' for char in playlist['title']).lower().replace("  ", " ")
                if playlist_name in playlist_vk:
                    playlist_id = playlist['id']
                    break
                    # q = QMessageBox.question(parent, "[VK] Что-то нашел", f"[VK] Нашел плейлист, его название верно?\n{playlist['title']}", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
                    # if q == QMessageBox.Yes:
                    #     playlist_id = playlist['id']
                    #     break
                    # elif q == QMessageBox.No:
                    #     continue
                    # else:
                    #     return False, False
        if not playlist_id:
            QMessageBox.information(None, "[VK] Информация", "[VK] Не нашел плейлист")
            return False, False
        post_id = None
        for i in range(10):
            posts = self.vk.wall.get(owner_id=self.group_id, count=70, offset=i*71)
            if not len(posts['items']):
                return False, False
            for post in posts['items']:
                post_text = post['text'].split('\n')[0]
                clean_post_text = ''.join(char if char not in string.punctuation else ' ' for char in post_text).lower().replace("  ", " ")
                if playlist_name in clean_post_text:
                    return post['id'], playlist_id, playlist['title'], post_text
                    q = QMessageBox.question(parent, "[VK] Что-то нашел", f"[VK] Этот ли прошлый пост?\n{post_text}", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
                    if q == QMessageBox.Yes:
                        return 
                    elif q == QMessageBox.No:
                        continue
                    else:
                        return False, False
        if not post_id:
            QMessageBox.warning(None, "[VK] Ошибка", "[VK] Не найден нужный пост, смените название папки для более точного названия, либо пост был сделан более 2-3 месяцев назад.")
            return False, False
        
    def upload_vk_dorama(self, file_path, file_path_pic, playlist_id, vk_post_id, name_file, select_dub, check_novideo_vk):
        try:
            self.ping_timmer = Connect().find_user_uid(Config().get_uid_program())[2]
            if check_novideo_vk == False:
                videos = self.vk.video.get(owner_id=self.group_id, album_id=playlist_id)
                last_video_title = videos['items'][0]['title']
                match = re.search(r'(\d+)\s+серия', last_video_title)
                if match:
                    new_title = last_video_title.replace(match.group(1), name_file)
                else:
                    print("Не смог изменить цифру в названии видео.")
                    return None #TODO не нашел цифру
                upload = VkUpload(self.vk_session)
                video = upload.video(file_path, group_id=abs(self.group_id), name=new_title, album_id=playlist_id)
                video_id = video['video_id']
                self.vk.video.save(group_id=abs(self.group_id), video_id=video_id)
                attachments = f'video{self.group_id}_{video_id}'
                if file_path_pic != '' or file_path_pic is not None:
                    if os.path.exists("assets/vk_storage.json"):
                        try:
                            with sync_playwright() as playwright:
                                browser = playwright.chromium.launch(headless=True)
                                context = browser.new_context(storage_state="assets/vk_storage.json")
                                page = context.new_page()
                                page.goto("https://vk.com/")
                                if page.url.format() == "https://vk.com/":
                                    # TODO ошибка
                                    os.remove("assets/vk_acc_cookies.json")
                                    context.close()
                                    browser.close()
                                else:
                                    page.goto(f"https://vk.com/{attachments}")
                                    main_locator = page.locator("#mv_main_info")
                                    main_locator.get_by_text("Ещё").click()
                                    main_locator.get_by_role("link", name="Редактировать").click()
                                    with page.expect_file_chooser() as fc_info:
                                        page.locator(".ThumbChooser__uploadStub").click()
                                    file_chooser = fc_info.value
                                    file_chooser.set_files(f"{file_path_pic}")
                                    time.sleep(2)
                                    page.get_by_role("button", name="Сохранить").click()
                                    time.sleep(2)
                                    context.close()
                                    browser.close()
                        except Exception as e:
                            log_config.setup_logger().exception(e)
            else:
                upload = vk_api.VkUpload(self.vk_session)
                photo = upload.photo_wall(f'{file_path_pic}')[0]
                attachments = f'photo{photo["owner_id"]}_{photo["id"]}'
            post = self.vk.wall.getById(posts=f'{self.group_id}_{vk_post_id}')
            post_text = post[0]['text']
            first_line = post_text.split('\n')[0]
            match = re.search(r'(\d+)\s*серия', first_line)
            if match:
                new_first_line = re.sub(r'(\d+)\s*серия', f'{name_file} серия', first_line)
                new_post_text = post_text.replace(first_line, new_first_line)
                if select_dub:
                    pattern = r"(?<=Роли озвучивали: ).*"
                    new_post_text = re.sub(pattern, select_dub, new_post_text)
                pattern = r"(?<=Тайминг и сведение: ).*"
                new_post_text = re.sub(pattern, str(self.ping_timmer), new_post_text)
            post = self.vk.wall.post(owner_id=self.group_id, message=new_post_text, attachments=attachments)
            self.vk.likes.add(owner_id=self.group_id, type='post', item_id=post['post_id'])
            return True
        except Exception as e:
            log_config.setup_logger().exception(e)
            traceback.print_exc()
            return False
                
        
        
        