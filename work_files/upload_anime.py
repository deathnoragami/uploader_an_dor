from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import QMessageBox

import work_files.upload_anime_sftp as upload_anime_sftp
from work_files.database_title import DatabaseManager
from work_files.upload_anime_sftp import SFTPManager
import os
from work_files.post_animaunt import PostAnimaunt
from work_files.post_vk import VkPostAnime
from work_files.dubbers import Dubbers

class UploadSignals(QObject):
    progress_changed = pyqtSignal(int, float, float, float)
    upload_signals = pyqtSignal(str)
    dirname_sftp_changed = pyqtSignal(str)
    post_signal = pyqtSignal(bool)


class UploadManager(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.signals = UploadSignals()
        self.worker = None
        self.dirname_sftp = None
        self.main_ui = main_window
        self.sftp_manager = SFTPManager()
        self.sftp_manager.signals.progress_changed.connect(self.signals.progress_changed)
        self.sftp_manager.signals.finished.connect(self.upload_finished)
        self.signals.dirname_sftp_changed.connect(self.set_dirname_sftp)


    def start_upload(self, file_path_image,
                    file_path_video,
                    check_sftp,
                    check_post_malf,
                    check_nolink,
                    check_post_site,
                    link_site_animaunt,
                    link_site_malf,                    
                    check_data):
        
        data = DatabaseManager().search_by_path_pic_anime(os.path.dirname(file_path_image))
        if not data or not data[0]["vk_post_id"]:
            post_id = VkPostAnime(name=os.path.basename(os.path.dirname(file_path_image))).search_post()
            if not post_id:
                return
        else:
            post_id = DatabaseManager().search_by_path_pic_anime(os.path.dirname(file_path_image))[0]['vk_post_id']
        select_dub = Dubbers().select_checkboxes(self.main_ui)
        self.worker = UploadWorker(self.sftp_manager, self.main_ui, select_dub, file_path_image,
                              file_path_video, check_sftp,
                              check_post_malf, check_nolink, check_post_site, link_site_animaunt, link_site_malf, check_data, post_id)
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
        


    def upload_finished(self, dirname=None, time=None):
        self.signals.upload_signals.emit(time)
        self.signals.dirname_sftp_changed.emit(dirname)
        
    
    def upload_vk_finish(self, upload_sftp):
        self.signals.post_signal.emit(bool(upload_sftp))
    
        
    def set_dirname_sftp(self, dirname):
        self.worker.dirname_sftp = dirname
        

class UploadWorker(QThread):
    signals = UploadSignals()
    qmsg = pyqtSignal()
    

    def __init__(self, sftp_manager, main_ui, select_dub, file_path_image,
                    file_path_video, check_sftp,
                    check_post_malf, check_nolink, check_post_site, link_site_animaunt, link_site_malf, check_data, post_id):
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
        self.check_data = check_data
        self.dirname_sftp = None
        self.main_ui = main_ui
        self.select_dub = select_dub
        self.post_id = post_id


    def run(self):
        if self.check_data:
            dirname = DatabaseManager().search_by_path_pic_anime(os.path.dirname(self.file_path_image))[0]['folder_sftp']
        else:
            dirname = None
        upload_sftp = True
        name_file = os.path.basename(self.file_path_image)
        path_image = os.path.dirname(self.file_path_image)
        if self.file_path_video is not None:
            path_video = os.path.dirname(self.file_path_video)
            name_video = os.path.basename(self.file_path_video)
        else:
            path_video = None
            name_video = None
        name_folder = os.path.basename(path_image)
        
        
        if self.post_id == None:
            QMessageBox.warning(None, "Ошибка", "Не найден нужный пост, смените название папки для более точного названия, либо пост был сделан более 2-3 месяцев назад.")
        if self.file_path_video is not None and self.check_sftp:
            upload_sftp = self.sftp_manager.upload_file(dirname, self.file_path_video, name_folder)
        if upload_sftp:
            if self.check_post_malf:
                post = PostAnimaunt(self.link_site_animaunt, self.link_site_malf, name_file)
            if self.check_post_site:
                post = PostAnimaunt(self.link_site_animaunt, self.link_site_malf, name_file, name_video)  
            VkPostAnime(check_nolink=self.check_nolink, path_image=self.file_path_image, post_id=self.post_id, number=name_file, select_dub=self.select_dub).post_vk()
            # заливка только в вк
            if self.check_data == False:
                dbm = DatabaseManager()
                dbm.add_entry(path_image, path_video, self.dirname_sftp, self.check_sftp, self.check_post_malf, self.check_nolink, self.check_post_site, self.link_site_animaunt, self.post_id, "anime", self.link_site_malf)
        self.signals.post_signal.emit(bool(upload_sftp))

        