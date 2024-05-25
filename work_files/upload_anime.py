from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import QMessageBox

from handle.parse_maunt import ParseMaunt
from work_files.database_title import DataBase
from work_files.upload_anime_sftp import SFTPManager
import os
import log_config
from work_files.post_animaunt import PostAnimaunt
from work_files.post_vk import VkPostAnime
import custom_widget.logger_tg as tg


class UploadSignals(QObject):
    progress_changed = pyqtSignal(int, float, float, float)
    finish_upload = pyqtSignal(bool, str)
    worker_finish_upload = pyqtSignal(bool, str)


class UploadManager(QThread):
    def __init__(self, main_ui):
        super().__init__()
        self.signals = UploadSignals()
        self.worker = None
        self.main_ui = main_ui
        self.dirname_sftp = None
        self.sftp_manager = SFTPManager()
        self.sftp_manager.signals.progress_changed.connect(self.signals.progress_changed)

    def start_upload(self, file_path_image,
                     file_path_video,
                     check_sftp,
                     check_post_malf,
                     check_nolink,
                     check_post_site,
                     link_site_animaunt,
                     link_site_malf,
                     select_dub,
                     name_user):
        """Класс для загрузки аниме
        Args:
            file_path_image (str): Полный пусть до файла картинки
            file_path_video (str): Полный пусть до файла видео
            check_sftp (bool): Чекбокс загрузки на сервер
            check_post_malf (bool): Чекбокс для поста на малфурик
            check_nolink (bool): Чекбокс для поста в вк без ссылок
            check_post_site (bool): Чекбокс для поста на анимаунт
            link_site_animaunt (str): Ссылка на сайт анимаунт
            link_site_malf (str): Ссылка на сайт малфурик
        """
        try:
            if file_path_video is not None:
                folder_file_path_video = os.path.dirname(file_path_video)
            else:
                folder_file_path_video = None
            if file_path_image is not None:
                folder_file_path_image = os.path.dirname(file_path_image)
                base_name = os.path.basename(os.path.dirname(file_path_image))
            with DataBase() as db:
                data = db.search_by_path_pic_anime(folder_file_path_image)
                if data != []:
                    if check_sftp == True and data[0][4] == 0:
                        self.signals.finish_upload.emit(False, "Ищу папку на сервере...")
                        dirname_sftp = self.search_folder_sftp(base_name)
                        if dirname_sftp is False:
                            self.signals.finish_upload.emit(True, "Не нашел папку на сервере.")
                            return
                    else:
                        dirname_sftp = data[0][3]
                    post_id = data[0][10]
                    db.update_anime(folder_file_path_image, folder_file_path_video, dirname_sftp, check_sftp,
                                    check_post_malf,
                                    check_nolink, check_post_site, link_site_animaunt, link_site_malf)
                else:
                    self.signals.finish_upload.emit(False, "Ищу нужный пост...")
                    post_id = self.search_post_vk(base_name)
                    if post_id is None:
                        self.signals.finish_upload.emit(True, "Не нашел нужный пост.")
                        return
                    if check_sftp:
                        self.signals.finish_upload.emit(False, "Ищу папку на сервере...")
                        dirname_sftp = self.search_folder_sftp(base_name)
                        if dirname_sftp is False:
                            self.signals.finish_upload.emit(True, "Не нашел папку.")
                            return
                    else:
                        dirname_sftp = None

                    db.add_anime(folder_file_path_image, folder_file_path_video, dirname_sftp,
                                 check_sftp, check_post_malf, check_nolink, check_post_site,
                                 link_site_animaunt, post_id, link_site_malf)

            try:
                self.worker.signals.worker_finish_upload.disconnect(self.signals.finish_upload)
            except:
                pass

            self.worker = UploadWorker(self.sftp_manager, self.main_ui, select_dub, file_path_image,
                                       file_path_video, check_sftp,
                                       check_post_malf, check_nolink, check_post_site, link_site_animaunt,
                                       link_site_malf, post_id, dirname_sftp, name_user)
            self.worker.signals.worker_finish_upload.connect(self.signals.finish_upload)
            self.worker.start()
        except Exception as e:
            log_config.setup_logger().exception(e)

    def search_post_vk(self, name):
        post_id = VkPostAnime(name=name).search_post()
        return post_id

    def search_folder_sftp(self, name):
        dirname_sftp = SFTPManager().search_folder_sftp(name)
        return dirname_sftp


class UploadWorker(QThread):
    signals = UploadSignals()

    def __init__(self, sftp_manager, main_ui, select_dub, file_path_image,
                 file_path_video, check_sftp,
                 check_post_malf, check_nolink, check_post_site, link_site_animaunt, link_site_malf, post_id,
                 dirname_sftp, name_user):
        super().__init__()
        self.sftp_manager = sftp_manager
        self.file_path_image = file_path_image
        self.file_path_video = file_path_video
        self.check_sftp = check_sftp
        self.check_post_malf = check_post_malf
        self.check_nolink = check_nolink
        self.check_post_site = check_post_site
        self.link_site_animaunt = link_site_animaunt
        self.link_site_malf = link_site_malf
        self.dirname_sftp = None
        self.main_ui = main_ui
        self.select_dub = select_dub
        self.post_id = post_id
        self.dirname_sftp = dirname_sftp
        self.name_user = name_user

    def run(self):
        try:
            nama_dir = os.path.basename(os.path.dirname(self.file_path_image))
            name_file = os.path.basename(self.file_path_image)
            if self.file_path_video is not None:
                name_video = os.path.basename(self.file_path_video)
            else:
                name_video = None
            if self.file_path_video is not None and self.check_sftp and self.dirname_sftp is not None:
                upload_sftp, time = self.sftp_manager.upload_file(self.dirname_sftp, self.file_path_video)
                if upload_sftp:
                    self.signals.worker_finish_upload.emit(False, f"{nama_dir} загружено на сервер в {time}")
                else:
                    self.signals.worker_finish_upload.emit(True, f"{nama_dir} ошибка загрузки на сервер")
            if self.check_post_malf:
                pass
                # TODO: Дописать когда добавлю на малф
            if self.check_post_site:
                data_time = self.main_ui.ui.dateEdit.date().toString("yyyy-MM-dd")
                # post = PostAnimaunt(self.link_site_animaunt, name_file, name_video,
                #                     data_time).post()
                post = ParseMaunt().update_seria_maunt(self.link_site_animaunt, int(name_file.split('.')[0]), 
                                                       data_time, name_video)
                if post == True:
                    self.signals.worker_finish_upload.emit(False, f"{nama_dir} запощен на сайт.")
                else:
                    QMessageBox.warning(None, "Ошибка", "Ошибка в публикации на сайте!")
                    self.signals.worker_finish_upload.emit(True, f"{nama_dir} ошибка при посте на сайт.")
                    return
            post_vk = VkPostAnime(check_nolink=self.check_nolink, path_image=self.file_path_image, post_id=self.post_id,
                                  number=name_file, select_dub=self.select_dub).post_vk()
            if post_vk:
                if self.dirname_sftp:
                    name = self.dirname_sftp.split("|")[0].strip()
                else:
                    name = nama_dir
                self.signals.worker_finish_upload.emit(False, f"{nama_dir} сделан пост в ВК.")
                tg.main('logger', self.name_user, name, name_file)
                self.signals.worker_finish_upload.emit(True, f"{nama_dir} загрузка завершена.")
            else:
                self.signals.worker_finish_upload.emit(True, f"{nama_dir} ошибка при посте в ВК.")
        except Exception as e:
            log_config.setup_logger().exception(e)
            self.signals.worker_finish_upload.emit(True, f"{nama_dir} ошибка при посте в ВК.")
            
