from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import QMessageBox

from work_files.dubbers import Dubbers

class UploadManagerDorama(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.worker = None
        self.dirname_sftp = None
        self.main_ui = main_window

    def start_upload(self, file_path_image,
                    file_path_video,
                    check_sftp,
                    check_post_malf,
                    check_nolink,
                    check_post_site,
                    link_site_animaunt,
                    link_site_malf,                    
                    check_data):
        
        select_dub = Dubbers().select_checkboxes(self.main_ui)
        self.worker = UploadWorkerDorama(self.sftp_manager, self.main_ui, select_dub, file_path_image,
                              file_path_video, check_sftp,
                              check_post_malf, check_nolink, check_post_site, link_site_animaunt, link_site_malf, check_data, post_id, dirname_sftp)
        self.worker.start()
        
    
class UploadWorkerDorama(QThread):
    def __init__(self):
        