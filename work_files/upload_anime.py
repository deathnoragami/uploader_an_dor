from PyQt5.QtCore import QObject, pyqtSignal, QThread

import work_files.upload_anime_sftp as upload_anime_sftp
from work_files.database_title import DatabaseManager
from work_files.upload_anime_sftp import SFTPManager
import os
from work_files.post_animaunt import PostAnimaunt

class UploadSignals(QObject):
    progress_changed = pyqtSignal(int, float, float, float)
    upload_signals = pyqtSignal(str)
    dirname_sftp_changed = pyqtSignal(str)
    post_signal = pyqtSignal(bool)


class UploadManager(QObject):
    def __init__(self):
        super().__init__()
        self.signals = UploadSignals()
        self.post_signal = pyqtSignal()
        self.worker = None
        self.dirname_sftp = None
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
        self.worker = UploadWorker(self.sftp_manager, file_path_image,
                              file_path_video, check_sftp,
                              check_post_malf, check_nolink, check_post_site, link_site_animaunt, link_site_malf, check_data)
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
    

    def __init__(self, sftp_manager, file_path_image,
                    file_path_video, check_sftp,
                    check_post_malf, check_nolink, check_post_site, link_site_animaunt, link_site_malf, check_data):
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


    def run(self):
        if self.check_data:
            dirname = DatabaseManager().search_by_path_pic_anime(os.path.dirname(self.file_path_image))[0]['folder_sftp']
        else:
            dirname = None
        upload_sftp = True
        name_file = os.path.basename(self.file_path_image)
        path_image = os.path.dirname(self.file_path_image)
        path_video = os.path.dirname(self.file_path_video) if self.file_path_video is not None else None
        name_folder = os.path.basename(path_image)
        if self.file_path_video is not None and self.check_sftp:
            upload_sftp = self.sftp_manager.upload_file(dirname, self.file_path_video, name_folder)
        if upload_sftp:
            if self.check_post_malf:
                post = PostAnimaunt(self.link_site_animaunt, self.link_site_malf, name_file)
            if self.check_post_site:
                post = PostAnimaunt(self.link_site_animaunt, self.link_site_malf, name_file)  
            
                # upload_anime_sftp()
            
            # заливка только в вк
            if self.check_data == False:
                dbm = DatabaseManager()
                dbm.add_entry(path_image, path_video, self.dirname_sftp, self.check_sftp, self.check_post_malf, self.check_nolink, self.check_post_site, self.link_site_animaunt, "anime", self.link_site_malf)
            #self.finished.emit()
        self.signals.post_signal.emit(bool(upload_sftp))

        