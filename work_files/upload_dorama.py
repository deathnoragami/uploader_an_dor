from PyQt5.QtCore import QObject, pyqtSignal, QThread, QCoreApplication
from PyQt5.QtWidgets import QMessageBox

from work_files.dubbers import Dubbers
from work_files.database_title import DataBase
from work_files.upload_dorama_tg import UploadDoramaTg
from work_files.upload_dorama_vk import UploadDoramaVK
from work_files.upload_dorama_sftp import UploadDoramaSFTP
from work_files.post_dorama import PostDorama

import os
import time
import log_config

class UploadSignals(QObject):
    progress_changed = pyqtSignal(int, float, float, float)
    finish_upload = pyqtSignal(bool, str, bool)
    worker_finish_upload = pyqtSignal(bool, str, bool)
    ask = pyqtSignal(list, list, list, bool, dict)
    askk = pyqtSignal(list, list, bool, dict)
    worker_finish_sftp = pyqtSignal(str)
    finish_sftp = pyqtSignal(str)

class UploadManagerDorama(QThread):
    def __init__(self, main_window, file_path_image,
                    file_path_video,
                    check_sftp,
                    check_vk,
                    check_tg,
                    check_post_site,
                    link_site_animaunt,
                    link_site_malf,                    
                    timming_list,
                    check_novideo_vk, 
                    select_dub):
        super().__init__()
        self.signals = UploadSignals()
        self.worker = None
        self.dirname_sftp = None
        self.main_ui = main_window
        self.sftp_manager = UploadDoramaSFTP()
        self.sftp_manager.signals.progress_changed.connect(self.signals.progress_changed)
        self.tg_manager = UploadDoramaTg()
        self.tg_manager.signals.progress_changed.connect(self.signals.progress_changed) 
        self.file_path_image = file_path_image
        self.file_path_video = file_path_video
        self.check_sftp = check_sftp
        self.check_vk = check_vk
        self.check_tg = check_tg
        self.check_post_site = check_post_site
        self.link_site_animaunt = link_site_animaunt
        self.link_site_malf = link_site_malf                  
        self.timming_list = timming_list
        self.check_novideo_vk = check_novideo_vk
        self.select_dub  = select_dub   

        self.signals.askk.connect(self.start_thread)

    def run(self):
        try:
            name = os.path.basename(os.path.dirname(self.file_path_video))
            if self.file_path_image is not None:
                file_path_image_folder = os.path.dirname(self.file_path_image)
            else:
                file_path_image_folder = None
            with DataBase() as db:
                update_values = {}
                data = db.search_by_path_video_dor(os.path.dirname(self.file_path_video))
                if data != []:
                    info_data = []
                    if self.check_tg == True and data[0][6] != self.check_tg:
                        self.signals.finish_upload.emit(False, f"Ищу пост в ТГ...", False)
                        tg_post_id, text_tg = UploadDoramaTg().seach_id_post(self.file_path_video)
                        if not tg_post_id:
                            self.signals.finish_upload.emit(True, f"{name} не нашел пост в ТГ.", False)
                            return
                        info_data.append(text_tg)
                        update_values["check_telegram"] = self.check_tg
                        update_values["tg_post_id"] = tg_post_id
                    elif self.check_tg == False and data[0][6] != self.check_tg:
                        info_data.append(None)
                        tg_post_id = None
                        update_values["check_telegram"] = self.check_tg
                        update_values["tg_post_id"] = "NULL"
                    else:
                        info_data.append(None)
                        tg_post_id = data[0][11]
                    if self.check_vk == True and data[0][5] != self.check_vk:
                        self.signals.finish_upload.emit(False, f"Ищу плейлист и пост в ВК...", False)
                        vk_post_id, vk_playlist_id, text_playlist, text_vk = UploadDoramaVK().search_vk_dorama(self.file_path_video)
                        if vk_playlist_id == False:
                            self.signals.finish_upload.emit(True, f"{name} ошибка при поиске в ВК.", False)
                            return
                        info_data.append(text_playlist)
                        info_data.append(text_vk)
                        update_values["vk_post_id"] = vk_post_id
                        update_values["vk_playlist_id"] = vk_playlist_id
                        update_values["check_vk"] = self.check_vk
                        update_values["check_novideo_vk"] = self.check_novideo_vk
                    elif self.check_vk == False and data[0][5] != self.check_vk:
                        vk_post_id = None
                        vk_playlist_id = None
                        info_data.append(None)
                        info_data.append(None)
                        update_values["vk_post_id"] = "NULL"
                        update_values["vk_playlist_id"] = "NULL"
                        update_values["check_vk"] = self.check_vk
                        update_values["check_novideo_vk"] = self.check_novideo_vk
                    else: 
                        info_data.append(None)
                        info_data.append(None)
                        vk_playlist_id = data[0][10]
                        vk_post_id = data[0][9]
                    if self.check_sftp == True and data[0][4] != self.check_sftp:
                        self.signals.finish_upload.emit(False, f"Ищу папку на сервере...", False)
                        folder_sftp = UploadDoramaSFTP().search_folder_sftp(self.file_path_video)
                        if not folder_sftp:
                            self.signals.finish_upload.emit(True, f"{name} не нашел папку на сервере.", False)
                            return
                        info_data.append(folder_sftp)
                        update_values["check_sftp"] = self.check_sftp
                        update_values["folder_sftp"] = folder_sftp
                    elif self.check_sftp == False and data[0][4] != self.check_sftp:
                        folder_sftp = None
                        info_data.append(None)
                        update_values["check_sftp"] = self.check_sftp
                    else:
                        info_data.append(None)
                        folder_sftp = data[0][3]
                    if self.check_post_site == True and data[0][7] != self.check_post_site:
                        update_values["check_site"] = self.check_post_site
                        update_values["link_second_site"] = self.link_site_animaunt
                        update_values["link_site"] = self.link_site_malf
                    elif self.check_post_site == False and data[0][7] != self.check_post_site:
                        update_values["check_site"] = self.check_post_site
                        update_values["link_second_site"] = self.link_site_animaunt
                        update_values["link_site"] = self.link_site_malf
                    if data[0][8] != self.check_novideo_vk:
                        update_values["check_novideo_vk"] = self.check_novideo_vk
                    # if update_values != {}:
                    #     db.update_dorama(os.path.dirname(self.file_path_video), update_values) 
                    
                    data_worker = [self.sftp_manager, self.tg_manager, self.file_path_video, self.file_path_image, 
                                vk_playlist_id, vk_post_id, tg_post_id, folder_sftp,
                                    self.check_sftp, self.check_tg, self.check_vk, self.check_post_site, 
                                    self.check_novideo_vk, self.link_site_animaunt, self.link_site_malf, 
                                    self.main_ui, self.select_dub, self.timming_list]   
                    self.signals.ask.emit([], info_data, data_worker, True, update_values)
                else:
                    info_data = []
                    if self.check_tg:
                        self.signals.finish_upload.emit(False, f"Ищу пост в ТГ...", False)
                        # QCoreApplication.processEvents()
                        tg_post_id, text_tg = UploadDoramaTg().seach_id_post(self.file_path_video)
                        if not tg_post_id:
                            self.signals.finish_upload.emit(True, f"{name} не нашел пост в ТГ.", False)
                            return
                        else:
                            self.signals.finish_upload.emit(False, f"Нашел {text_tg}", False)
                        info_data.append(text_tg)
                    else:
                        tg_post_id = None
                        info_data.append(None)
                    if self.check_vk:
                        self.signals.finish_upload.emit(False, f"Ищу плейлист и пост в ВК...", False)
                        vk_post_id, vk_playlist_id, text_playlist, text_vk = UploadDoramaVK().search_vk_dorama(self.file_path_video)
                        if vk_playlist_id == False:
                            self.signals.finish_upload.emit(True, f"{name} ошибка при поиске в ВК.", False)
                            return
                        else:
                            self.signals.finish_upload.emit(False, f"Нашел {text_playlist}\n{text_vk}", False)
                        info_data.append(text_playlist)
                        info_data.append(text_vk)
                    else:
                        vk_post_id, vk_playlist_id = None, None
                        info_data.append(None)
                        info_data.append(None)
                    if self.check_sftp:
                        self.signals.finish_upload.emit(False, f"Ищу папку на сервере...", False)
                        # QCoreApplication.processEvents()
                        folder_sftp = UploadDoramaSFTP().search_folder_sftp(self.file_path_video)
                        if not folder_sftp:
                            self.signals.finish_upload.emit(True, f"{name} не нашел папку на сервере.", False)
                            return
                        else:
                            self.signals.finish_upload.emit(False, f"Нашел {folder_sftp}", False)
                        info_data.append(folder_sftp)
                    else:
                        folder_sftp = None
                        info_data.append(None)
                    data_entry = [os.path.dirname(self.file_path_video), file_path_image_folder, folder_sftp, self.check_sftp,
                                            self.check_vk, self.check_tg, self.check_post_site, self.check_novideo_vk, vk_post_id, vk_playlist_id,
                                            tg_post_id, self.link_site_malf, self.link_site_animaunt]
                    data_worker = [self.sftp_manager, self.tg_manager, self.file_path_video, self.file_path_image, 
                                vk_playlist_id, vk_post_id, tg_post_id, folder_sftp,
                                    self.check_sftp, self.check_tg, self.check_vk, self.check_post_site, 
                                    self.check_novideo_vk, self.link_site_animaunt, self.link_site_malf, 
                                    self.main_ui, self.select_dub, self.timming_list]
                    self.signals.ask.emit(data_entry, info_data, data_worker, False, {})
        except Exception as e:
            log_config.setup_logger().exception(e)

    def start_thread(self, data, data_worker, update, update_values):
        try:
            with DataBase() as db:
                if update == False:
                    db.add_dorama(*data)
                else:
                    if update_values != {}:
                        db.update_dorama(os.path.dirname(data_worker[2]), update_values)
            try:
                self.worker.signals.worker_finish_upload.disconnect(self.signals.finish_upload)
                self.worker.signals.worker_finish_sftp.disconnect(self.signals.finish_sftp)
            except:
                pass
            self.worker = UploadWorkerDorama(*data_worker)
            self.worker.signals.worker_finish_upload.connect(self.signals.finish_upload)
            self.worker.signals.worker_finish_sftp.connect(self.signals.finish_sftp)
            self.worker.start()
        except Exception as e:
            log_config.setup_logger().exception(e)
                  
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
            name = os.path.basename(os.path.dirname(self.file_path_video))
            name_file = os.path.splitext(os.path.basename(self.file_path_video))[0].lstrip('0').replace('x', '')
            if self.check_sftp:
                self.signals.worker_finish_upload.emit(False, f"Заливаю на сервер...", False)
                upload_sftp, sftp_time = self.sftp_manager.upload_sftp(self.file_path_video, self.folder_sftp)
                if upload_sftp:
                    self.signals.worker_finish_sftp.emit(f"{name} залита на сервер в {sftp_time}")
                else:
                    self.signals.worker_finish_upload.emit(True, f"{name} ошибка загрузки на сервер.", True)
                    return
            if self.check_tg:
                upload_tg = self.tg_manager.upload_tg(self.file_path_video, self.tg_post_id)
                if upload_tg:
                    self.signals.worker_finish_upload.emit(False, f"{name} залито в ТГ.", True)
                else:
                    self.signals.worker_finish_upload.emit(True, f"{name} ошибка загрузки в ТГ.", True)
                    return
            if self.check_vk:
                self.signals.worker_finish_upload.emit(False, f"Начинаю загрузку в ВК...", False)
                upload_vk = UploadDoramaVK().upload_vk_dorama(self.file_path_video, self.file_path_image, self.vk_playlist_id, self.vk_post_id, name_file, self.select_dub, self.check_novideo_vk)
                if upload_vk:
                    self.signals.worker_finish_upload.emit(False, f"{name} залито в ВК.", True)
                else:
                    self.signals.worker_finish_upload.emit(True, f"{name} ошибка загрузки в ВК.", True)
                    return
            if self.check_post_site:
                post_malf = PostDorama().post_malfurik(self.link_malf, name_file=os.path.basename(self.file_path_video), timming_list=self.timming_list)
                if post_malf == True:
                    self.signals.worker_finish_upload.emit(False, f"Запощен на сайт Малфурик.", True)
                    post_maunt = PostDorama().post_animaunt(self.main_ui.ui.check_timmer_dor.isChecked(), self.link_animaunt, name_file)
                    if post_maunt != True:
                        self.signals.worker_finish_upload.emit(True, f"Ошибка поста на Анимаунт.", True)
                        # QMessageBox.warning(None, "Ошибка", f"Ошибка при посте на анимаунт")
                    else:
                        self.signals.worker_finish_upload.emit(False, f"Запощен на сайт Анимаунт.", True)
                else:
                    self.signals.worker_finish_upload.emit(True, f"Ошибка поста на Малфурик.", True)
                    # QMessageBox.warning(None, "Ошибка", f"Ошибка при посте на малфурик")
            self.signals.worker_finish_upload.emit(True, f"{name} загрузка завершена.", False)

        except Exception as e:
            log_config.setup_logger().exception(e)
            self.signals.worker_finish_upload.emit(True, f"{name} ошибка загрузки {e}", True)
            return