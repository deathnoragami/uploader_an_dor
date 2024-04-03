from PyQt5.QtCore import QObject, pyqtSignal, QThread, QEventLoop, pyqtSlot
from PyQt5.QtWidgets import QMessageBox

import work_files.upload_anime_sftp as upload_anime_sftp
from work_files.database_title import DataBase
from work_files.upload_anime_sftp import SFTPManager
import os
from work_files.post_animaunt import PostAnimaunt
from work_files.post_vk import VkPostAnime
from work_files.dubbers import Dubbers

class UploadSignals(QObject):
    search_signal = pyqtSignal(str)

    progress_changed = pyqtSignal(int, float, float, float)
    upload_signals = pyqtSignal(str)
    post_signal = pyqtSignal(bool)


class UploadManager(QThread):
    def __init__(self):
        super().__init__()
        self.signals = UploadSignals()
        self.worker = None
        self.dirname_sftp = None
        self.sftp_manager = SFTPManager()
        self.sftp_manager.signals.progress_changed.connect(self.signals.progress_changed)
        self.sftp_manager.signals.finished.connect(self.upload_finished)

    def start_upload(self, file_path_image=None,
                    file_path_video=None,
                    check_sftp=None,
                    check_post_malf=None,
                    check_nolink=None,
                    check_post_site=None,
                    link_site_animaunt=None,
                    link_site_malf=None):
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
        if file_path_video is not None:
            file_path_video = os.path.dirname(file_path_video)
        if file_path_image is not None:
            file_path_image = os.path.dirname(file_path_image)
            base_name = os.path.basename(file_path_image)
        with DataBase() as db:
            data = db.search_by_path_pic_anime(file_path_image)
            if data != []:
                if check_sftp != data[0][4]:
                    self.signals.search_signal.emit("Ищу папку на сервере...")
                    dirname_sftp = self.search_folder_sftp(base_name)
                    if dirname_sftp is False:
                        self.signals.post_signal.emit(False)
                        return
                else:
                    dirname_sftp = data[0][3]
                db.update_anime(os.path.dirname(file_path_image), file_path_video, dirname_sftp, check_sftp, check_post_malf, 
                                check_nolink, check_post_site, link_site_animaunt, link_site_malf)
            else:
                self.signals.search_signal.emit("Ищу нужный пост...")
                post_id = self.search_post_vk(base_name)
                if post_id is None:
                    self.signals.post_signal.emit(False)
                    return
                if check_sftp:
                    self.signals.search_signal.emit("Ищу папку на сервере...")
                    dirname_sftp = self.search_folder_sftp(base_name)
                    if dirname_sftp is False:
                        self.signals.post_signal.emit(False)
                        return
                else:
                    dirname_sftp = None

                
                db.add_anime(os.path.dirname(file_path_image), file_path_video, dirname_sftp, 
                    check_sftp, check_post_malf, check_nolink, check_post_site,
                    link_site_animaunt, post_id, link_site_malf)

        select_dub = Dubbers().select_checkboxes(self.main_ui)
        self.worker = UploadWorker(self.sftp_manager, self.main_ui, select_dub, file_path_image,
                              file_path_video, check_sftp,
                              check_post_malf, check_nolink, check_post_site, link_site_animaunt, link_site_malf, post_id, dirname_sftp)
        try:
            self.worker.signals.post_signal.disconnect(self.upload_vk_finish)
            self.worker.signals.dirname_sftp_changed.disconnect(self.set_dirname_sftp)
            self.worker.signals.progress_changed.disconnect(self.signals.progress_changed)
            self.worker.signals.upload_signals.disconnect(self.upload_finished)
        except Exception as e:
            pass
        
        self.worker.signals.dirname_sftp_changed.connect(self.set_dirname_sftp)
        self.worker.signals.progress_changed.connect(self.signals.progress_changed)
        self.worker.signals.upload_signals.connect(self.upload_finished)
        self.worker.signals.post_signal.connect(self.upload_vk_finish)
        self.worker.start()
   
    def search_post_vk(self, name):
        post_id = VkPostAnime(name=name).search_post()
        return post_id
    
    def search_folder_sftp(self, name):
        dirname_sftp = SFTPManager().search_folder_sftp(name)
        return dirname_sftp

    def upload_finished(self, dirname=None, time=None):
        self.signals.upload_signals.emit(time)
        self.signals.dirname_sftp_changed.emit(dirname)
        
    
    def upload_vk_finish(self, upload_sftp):
        self.signals.post_signal.emit(bool(upload_sftp))
          
class UploadWorker(QThread):
    signals = UploadSignals()
    qmsg = pyqtSignal()
    

    def __init__(self, sftp_manager, main_ui, select_dub, file_path_image,
                    file_path_video, check_sftp,
                    check_post_malf, check_nolink, check_post_site, link_site_animaunt, link_site_malf, post_id, dirname_sftp):
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

    def run(self):
        upload_sftp = True
        name_file = os.path.basename(self.file_path_image)
        path_image = os.path.dirname(self.file_path_image)
        if self.file_path_video is not None:
            path_video = os.path.dirname(self.file_path_video)
            name_video = os.path.basename(self.file_path_video)
        else:
            path_video = None
            name_video = None        
        
        if self.file_path_video is not None and self.check_sftp and self.dirname_sftp is not None:
            upload_sftp = self.sftp_manager.upload_file(self.dirname_sftp, self.file_path_video)
        if upload_sftp:
            if self.check_post_malf:
                post = PostAnimaunt(self.link_site_animaunt, self.link_site_malf, name_file)
            if self.check_post_site:
                data_time = self.main_ui.ui.dateEdit.date().toString("yyyy-MM-dd")
                post = PostAnimaunt(self.link_site_animaunt, self.link_site_malf, name_file, name_video, data_time).post()
                if post == True:
                    pass
                else:
                    QMessageBox.warning(None, "Ошибка", "Ошибка в публикации на сайте!")
                    self.signals.post_signal.emit(False)
                    return
            VkPostAnime(check_nolink=self.check_nolink, path_image=self.file_path_image, post_id=self.post_id, number=name_file, select_dub=self.select_dub).post_vk()

        self.signals.post_signal.emit(bool(upload_sftp))

