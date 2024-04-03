from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import QMessageBox

from work_files.dubbers import Dubbers
from work_files.database_title import DataBase
from work_files.upload_dorama_tg import UploadDoramaTg
from work_files.upload_dorama_vk import UploadDoramaVK
from work_files.upload_dorama_sftp import UploadDoramaSFTP
from work_files.post_dorama import PostDorama

import os
import time

class UploadSignals(QObject):
    progress_changed = pyqtSignal(int, float, float, float)
    finished_upload_sftp = pyqtSignal(str, str)
    finished_upload_tg = pyqtSignal(bool)
    finish_all = pyqtSignal(str)
    finish = pyqtSignal(bool, str)
    
class UploadManagerDorama(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.signals = UploadSignals()
        self.worker = None
        self.dirname_sftp = None
        self.main_ui = main_window
        self.sftp_manager = UploadDoramaSFTP()
        self.sftp_manager.signals.progress_changed.connect(self.signals.progress_changed)
        self.sftp_manager.signals.finished.connect(self.signals.finished_upload_sftp)
        self.tg_manager = UploadDoramaTg()
        self.tg_manager.signals.progress_changed.connect(self.signals.progress_changed)
        self.tg_manager.signals.finished.connect(self.signals.finished_upload_tg)
        

    def start_upload(self, file_path_image,
                    file_path_video,
                    check_sftp,
                    check_vk,
                    check_tg,
                    check_post_site,
                    link_site_animaunt,
                    link_site_malf,                    
                    check_data,
                    timming_list,
                    check_novideo_vk, 
                    select_dub):
        if file_path_image is not None:
            file_path_image_folder = os.path.dirname(file_path_image)
            print(file_path_image_folder)
            print(file_path_image)
        if check_data:
            with DataBase() as db:
                update_values = {}
                data = db.search_by_path_video_dor(os.path.dirname(file_path_video))
                if check_tg and data[0][6] != check_tg:
                    tg_post_id = UploadDoramaTg().seach_id_post(file_path_video)
                    if not tg_post_id:
                        self.signals.finish.emit(False)
                        return
                    update_values.update({"check_telegram"}, check_tg)
                    update_values.update({"tg_post_id"}, tg_post_id)
                else:
                    tg_post_id = data[0][10]
                if check_vk and data[0][5] != check_vk:
                    vk_post_id, vk_playlist_id = UploadDoramaVK().search_vk_dorama(file_path_video)
                    if not vk_post_id and not vk_playlist_id:
                        self.signals.finish.emit(False)
                        return
                    update_values["vk_post_id"] = vk_post_id
                    update_values["vk_playlist_id"] = vk_playlist_id
                    update_values["check_vk"] = check_vk
                else: 
                    vk_playlist_id = data[0][9]
                    vk_post_id = data[0][8]
                if check_sftp and data[0][6] != check_sftp:
                    folder_sftp = UploadDoramaSFTP().search_folder_sftp(file_path_video)
                    if not folder_sftp:
                        self.signals.finish.emit(False)
                        return
                    update_values.update({"check_sftp"}, check_sftp)
                    update_values.update({"folder_sftp"}, folder_sftp)
                else:
                    folder_sftp = data[0][3]
                if update_values != {}:
                    db.update_dorama(os.path.dirname(file_path_video), update_values)
        else:
            if check_tg:
                tg_post_id = UploadDoramaTg().seach_id_post(file_path_video)
                if not tg_post_id:
                    self.signals.finish.emit(False)
                    return
            else:
                tg_post_id = None
            if check_vk:
                try:
                    vk_post_id, vk_playlist_id = UploadDoramaVK().search_vk_dorama(file_path_video)
                except TypeError as e:
                    self.signals.finish.emit(False)
                    return
            else:
                vk_post_id, vk_playlist_id = None, None
            if check_sftp:
                folder_sftp = UploadDoramaSFTP().search_folder_sftp(file_path_video)
                if not folder_sftp:
                    self.signals.finish.emit(False)
                    return
            else:
                folder_sftp = None
        if not check_data:
            with DataBase() as db:
                db.add_dorama(os.path.dirname(file_path_video), file_path_image_folder, folder_sftp, check_sftp,
                                    check_vk, check_tg, check_post_site, check_novideo_vk, vk_playlist_id,
                                    vk_post_id, tg_post_id, link_site_malf, link_site_animaunt)
        self.worker = UploadWorkerDorama(self.sftp_manager, self.tg_manager, file_path_video, file_path_image, vk_playlist_id, vk_post_id, tg_post_id, folder_sftp,
                                         check_sftp, check_tg, check_vk, check_post_site, check_novideo_vk, link_site_animaunt, link_site_malf, self.main_ui, select_dub, timming_list)
        self.worker.signals.finish_all.connect(self.all_post)
        self.worker.start()
    
    def all_post(self, text):  
        self.signals.finish.emit(True, text)
                  
class UploadWorkerDorama(QThread):
    signals = UploadSignals()
    def __init__(self, sftp_manager, tg_manager, file_path_video, file_path_image, vk_playlist_id, vk_post_id, tg_post_id, folder_sftp,
                        check_sftp, check_tg, check_vk, check_post_site, check_novideo_vk, link_site_animaunt, link_site_malf, main_ui, select_dub, timming_list):
        super().__init__()
        self.sftp_manager = sftp_manager
        self.tg_manager = tg_manager
        self.file_path_video = file_path_video
        self.file_path_image = file_path_image
        self.vk_playlist_id = vk_playlist_id
        self.vk_post_id = vk_post_id
        self.tg_post_id = tg_post_id
        self.folder_sftp = folder_sftp
        self.check_sftp = check_sftp
        self.check_tg = check_tg
        self.check_vk = check_vk
        self.check_post_site = check_post_site
        self.check_novideo_vk = check_novideo_vk
        self.link_animaunt = link_site_animaunt
        self.link_malf = link_site_malf
        self.main_ui = main_ui
        self.select_dub = select_dub
        self.timming_list = timming_list

        
    def run(self):
        try:
            name_file = os.path.splitext(os.path.basename(self.file_path_video))[0].lstrip('0').replace('x', '')
            if self.check_sftp:
                self.sftp_manager.upload_sftp(self.file_path_video, self.folder_sftp)
            if self.check_tg:
                self.tg_manager.upload_tg(self.file_path_video, self.tg_post_id)
            if self.check_vk:
                UploadDoramaVK().upload_vk_dorama(self.file_path_video, self.file_path_image, self.vk_playlist_id, self.vk_post_id, name_file, self.select_dub, self.check_novideo_vk)
                # self.main_ui.ui.logging_upload.append("Запощено в ВК")
            if self.check_post_site:
                post_malf = PostDorama().post_malfurik(self.link_malf, name_file=os.path.basename(self.file_path_video), timming_list=self.timming_list)
                if post_malf == True:
                    post_maunt = PostDorama().post_animaunt(self.main_ui.ui.check_timmer_dor.isChecked(), self.link_animaunt, name_file)
                    if post_maunt != True:
                        self.signals.finish_all.emit(os.path.basename(os.path.dirname(self.file_path_video)))
                        QMessageBox.warning(None, "Ошибка", f"Ошибка при посте на анимаунт")
                else:
                    self.signals.finish_all.emit(os.path.basename(os.path.dirname(self.file_path_video)))
                    QMessageBox.warning(None, "Ошибка", f"Ошибка при посте на малфурик")
                    return
                self.main_ui.ui.logging_upload.append("Запощено на сайт")
            self.signals.finish_all.emit(os.path.basename(os.path.dirname(self.file_path_video)))

        except Exception as e:
            self.signals.finish_all.emit(os.path.basename(os.path.dirname(self.file_path_video)))
            QMessageBox.warning(None, "Ошибка", f"Ошибка при постинге {e}")
            return