from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem, QDateEdit
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QSize, QTimer, QDate
from ui import Ui_MainWindow

from autorization.autorization_application.autorizade_app import AuthorizationApp
from autorization.autorization_vk.autorizade_vk import AuthorizationVK
from autorization.autorization_tg.autorizade_tg import AuthorizationTG
from autorization.autorization_server.autorizade_sftp import AutorizationServer
from autorization.autorization_animaunt.autorization_web_animaunt import Animaunt_web
from autorization.autorization_malfurik.autorization_web_malfurik import Malfurik_web
from autorization.autorization_vk_site.autorization_web_vk import AutorizationWebVK

from work_files.select_pic_anime import PictureSelectorAnime
from work_files.select_video_anime import VideoSelectorAnime
from work_files.select_video_dorama import VideoSelectorDorama
from work_files.select_pic_dorama import PictureSelectorDorama
from work_files.upload_anime import UploadManager
from work_files.upload_dorama import UploadManagerDorama
from work_files.post_dorama import PostDorama
from work_files.database_title import DatabaseManager
from work_files.dubbers import Dubbers
from work_files.download_fix_timming import FixTimming

import timming_pro.timming_main as timming

from version import VERSION_STRING
from config import Config

import sys
import os
import glob
import json
import pytz
import datetime
import re
import resource_path
from urllib.parse import unquote
from dotenv import load_dotenv

from qt_material import apply_stylesheet

import connect_firebase


load_dotenv(dotenv_path=resource_path.path(".env"))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(f"AUPAn {VERSION_STRING}")
        self.setWindowIcon(QIcon(resource_path.path("icon.ico")))
        self.center_screen()
        db = connect_firebase.Connect()

        ############## ОБНУЛЕНИЕ ПЕРЕМЕННЫХ #############################
        
        self.file_path_anime_pic = None
        self.file_path_anime_video = None
        self.file_path_dorama_pic = None
        self.file_path_dorama_video = None
        self.link_site_animaunt = None
        self.link_malf_anime = None
        
        #################################################################

        ################ ДАТА ###########################################
        self.ui.dateEdit.setButtonSymbols(QDateEdit.NoButtons)
        msk_timezone = pytz.timezone('Europe/Moscow')
        current_date_msk = datetime.datetime.now(msk_timezone)
        self.year = current_date_msk.year
        self.month = current_date_msk.month
        self.day = current_date_msk.day
        self.ui.dateEdit.setDate(QDate(self.year,  self.month, self.day))

        ########## ПРОВЕРКА АВТОРИЗАЦИИ ##################################

        user_autorization = False
        config = Config()
        uid = config.get_uid_program()
        if not uid == '':
            user_data = db.find_user_uid(uid)
            if user_data:
                self.ui.block_screen.hide()
                user_autorization = True

        if not user_autorization:
            self.ui.menu_vk.setDisabled(True)
            self.ui.menu_tg.setDisabled(True)
            self.ui.menu_server.setDisabled(True)
            self.ui.menu_animaunt.setDisabled(True)
            self.ui.menu_2.setDisabled(True)

        ##################################################################
    
        ########## Добавление чекбоксов дабберов #############################

        self.dub_data = db.get_dub_data()
        self.ui.scrollAreaWidgetContents.setLayout(QtWidgets.QVBoxLayout())
        sorted_result = sorted(self.dub_data, key=lambda x: x['id'])
        self.checkbox_vars = []
        for item in sorted_result:
            checkbox = QtWidgets.QCheckBox(item['id'])
            ping_value = item.get('ping', '')
            self.checkbox_vars.append((checkbox, ping_value, item['id']))
            self.ui.scrollAreaWidgetContents.layout().addWidget(checkbox)

        #####################################################################
        
        ###################### АКТИВАЦИЯ ВИДЖЕТОВ ###########################
        if Config().get_vk_token != "":
            self.ui.btn_pic_anime.setEnabled(True)
            self.ui.check_vk_dor.setEnabled(True)
        if os.path.exists("assets/my_session_tg.session"):
            self.ui.check_tg_dor.setEnabled(True)
        if user_data:
            if ('malf_pass' not in user_data or not user_data['malf_pass']) or ('malf_login' not in user_data or not user_data['malf_login']):
                pass
            else:
                self.ui.check_sftp_dor.setEnabled(True)
            if ('maunt_login' not in user_data or not user_data['maunt_login']) or ('maunt_pass' not in user_data or not user_data['maunt_pass']):
                pass
            else:
                self.ui.check_sftp_anime.setEnabled(True)
                self.ui.btn_video_anime.setEnabled(True)
        if os.path.exists("assets/animaunt_storage.json"):
            self.ui.check_post_site.setEnabled(True)
            if os.path.exists("assets/malfurik_storage.json"):
                self.ui.check_update_site_dor.setEnabled(True)
        if os.path.exists("assets/vk_storage.json"):
            self.ui.btn_chose_pic_dor.setEnabled(True)
        #####################################################################
        
        db.close()
        ################## ТАЙМИНГ ##################################  
             
        if os.path.exists("assets/timming.json"):
            with open("assets/timming.json", "r", encoding="UTF-8") as file:
                data_list = []
                for line in reversed(file.readlines()):
                    data = json.loads(line)
                    data_list.append(data)
            for item_data in data_list:
                item_text = f"{item_data['projectname']} Секв. {item_data['sequencename']}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, item_data)
                self.ui.list_timming.addItem(item)
        self.ui.list_timming.itemClicked.connect(self.get_timming)
        self.ui.btn_del_timming.clicked.connect(self.delete_select_timming)
        self.ui.btn_add_timming.clicked.connect(self.add_timming)
        self.ui.btn_open_timming.clicked.connect(self.chose_animation_open_timming)
        self.ui.textedit_timming_ad.mousePressEvent = lambda event: self.copy(event, self.ui.textedit_timming_ad)
        self.ui.textedit_name_ad.mousePressEvent = lambda event: self.copy(event, self.ui.textedit_name_ad)
        self.ui.btn_add_timming_malf.clicked.connect(self.post_malf)
        
        ####################################################################

        ############# МЕНЮ ВЕРНХЕЕ ####################################
        
        self.ui.menu_application.triggered.connect(AuthorizationApp)
        self.ui.menu_vk.triggered.connect(self.autorization_vk)
        self.ui.menu_tg.triggered.connect(self.autorization_tg)
        self.ui.menu_server.triggered.connect(self.autorization_sftp)
        
        self.ui.menu_animaunt.triggered.connect(self.autorization_animaunt_web)
        self.ui.menu_malfurik.triggered.connect(self.autorization_malfurik_web)
        self.ui.menu_vk_site.triggered.connect(self.autorization_vk_web)
        
        self.ui.menu_fix_timming.triggered.connect(FixTimming)

        #####################################################################

        ############### Аниме выбор, кнопки ###################################

        self.picture_selector_anime = PictureSelectorAnime()
        self.picture_selector_anime.picture_selected.connect(self.update_label_pic_anime)
        self.ui.btn_pic_anime.clicked.connect(self.select_picture_anime)

        self.video_selector_anime = VideoSelectorAnime()
        self.video_selector_anime.video_selected.connect(self.update_label_video_anime)
        self.ui.btn_video_anime.clicked.connect(self.select_video_anime)

        self.ui.btn_upload_anime.clicked.connect(self.start_work)
        self.upload_manager = UploadManager(self)
        self.upload_manager.signals.progress_changed.connect(self.update_progress)
        self.upload_manager.signals.upload_signals.connect(self.upload_finished)
        self.upload_manager.signals.post_signal.connect(self.upload_vk_finish)

        self.ui.check_malf_anime.stateChanged.connect(self.toggle_site_anime)
        
        #######################################################################

        ########################## ДОРАМЫ КНОПКИ ##############################
        
        self.video_selector_dorama = VideoSelectorDorama()
        self.video_selector_dorama.video_selected.connect(self.update_video_dorama)
        self.ui.btn_chose_video_dor.clicked.connect(self.select_video_dorama)
        
        self.pictute_selecor_dorama = PictureSelectorDorama()
        self.pictute_selecor_dorama.picture_selected.connect(self.update_picture_dorama)
        self.ui.btn_chose_pic_dor.clicked.connect(self.select_picture_dorama)
        
        self.upload_manager_dorama = UploadManagerDorama(self)
        self.upload_manager_dorama.signals.progress_changed.connect(self.update_progress_dor)
        self.upload_manager_dorama.signals.finished_upload_sftp.connect(self.finish_upload_sftp_dor)
        self.upload_manager_dorama.signals.finished_upload_tg.connect(self.finish_upload_tg_dor)
        self.upload_manager_dorama.signals.finish.connect(self.finish_dor)
        self.ui.btn_upload_dor.clicked.connect(self.start_work_dorama)
        
        self.ui.check_update_site_dor.stateChanged.connect(self.enable_timer_dor)
        
        #######################################################################      
        
        ######################### СДАЧА ДОРОГ #################################

        self.ui.line_id_chat.setText(Config().get_id_chat())
        self.ui.line_id_chat.textChanged.connect(self.save_id_chat)
        self.ui.btn_search_dubs.clicked.connect(self.btn_search_dub)
        self.ui.text_send_dub.mousePressEvent = lambda event: self.copy(event, self.ui.text_send_dub)

        #######################################################################

    ####################### ФУНКЦИИ ДЛЯ АВТОРИЗАЦИИ ###########################
    
    def autorization_vk(self):
        check = AuthorizationVK()
        if check:
            self.ui.btn_pic_anime.setEnabled(True)
            self.ui.check_vk_dor.setEnabled(True)
    
    def autorization_tg(self):
        check = AuthorizationTG()
        if check:
            self.ui.check_tg_dor.setEnabled(True)
            
    def autorization_sftp(self):
        AutorizationServer()
        uid = Config().get_uid_program()
        db = connect_firebase.Connect()
        user_data = db.find_user_uid(uid)
        print(user_data)
        db.close()
        if user_data:
            if ('malf_pass' not in user_data or not user_data['malf_pass']) or ('malf_login' not in user_data or not user_data['malf_login']):
                pass
            else:
                self.ui.check_sftp_dor.setEnabled(True)
            if ('maunt_login' not in user_data or not user_data['maunt_login']) or ('maunt_pass' not in user_data or not user_data['maunt_pass']):
                pass
            else:
                self.ui.check_sftp_anime.setEnabled(True)
                self.ui.btn_video_anime.setEnabled(True)
    
    def autorization_animaunt_web(self):
        Animaunt_web()
        if os.path.exists("assets/animaunt_storage.json"):
            self.ui.check_post_site.setEnabled(True)
            if os.path.exists("assets/malfurik_storage.json"):
                self.ui.check_update_site_dor.setEnabled(True)
    
    def autorization_malfurik_web(self):
        Malfurik_web()
        if os.path.exists("assets/malfurik_storage.json") and os.path.exists("assets/animaunt_storage.json"):
            self.ui.check_update_site_dor.setEnabled(True)
            
    def autorization_vk_web(self):
        AutorizationWebVK()
        if os.path.exists("assets/vk_storage.json"):
            self.ui.btn_chose_pic_dor.setEnabled(True)
            
        
    
    ###########################################################################



    ##################### ФУНКЦИИ ДЛЯ ТАЙМИНГОВ ###############################
    
    def copy(self, event, ui_text):
        if event.button() == Qt.LeftButton:
            text = ui_text.toPlainText()
            if text:
                QApplication.clipboard().setText(f'"{text}"')
 
    def add_timming(self):
        data = timming.add_timming()
        item_text = f"{data['projectname']} Секв. {data['sequencename']}"
        item = QListWidgetItem(item_text)
        item.setData(Qt.UserRole, data)
        self.ui.list_timming.insertItem(0, item)

    def get_timming(self, item):
        item_data = item.data(Qt.UserRole)
        times, name_ad = timming.format_timming(item_data)
        self.ui.textedit_timming_ad.setText(times)
        self.ui.textedit_name_ad.setText(name_ad)
        
    def delete_select_timming(self):
        selected_item = self.ui.list_timming.currentItem()
        if selected_item:
            item_data = selected_item.data(Qt.UserRole)
            self.ui.list_timming.takeItem(self.ui.list_timming.row(selected_item))
            with open("assets/timming.json", "r", encoding="UTF-8") as file:
                data_list = [json.loads(line) for line in file]
            data_list = [item for item in data_list if item != item_data]
            with open("assets/timming.json", "w", encoding="UTF-8") as file:
                for item in data_list:
                    json.dump(item, file, ensure_ascii=False)
                    file.write('\n')
    
    def chose_animation_open_timming(self):
        if self.height() == 499:
            self.animation_open_timming("open")
        else:
            self.animation_open_timming("close")
    
    def animation_open_timming(self, chose):
        self.chose = chose
                    
        if chose == "open":
            self.setMaximumHeight(681)
            end_height = 690
            btn_end_y = 633
            btn_text = "🠉"
        else:
            self.setMinimumHeight(499)
            end_height = 499
            btn_end_y = 440
            btn_text = "🠋"

        self.animation = QPropertyAnimation(self, b"size")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.setStartValue(QSize(self.size()))
        self.animation.setEndValue(QSize(self.width(), end_height))
        self.animation.start()

        self.btn_animation = QPropertyAnimation(self.ui.btn_open_timming, b"geometry")
        self.btn_animation.setDuration(500)
        self.btn_animation.setEasingCurve(QEasingCurve.InOutCubic) 
        self.btn_animation.setStartValue(QRect(self.ui.btn_open_timming.x(), self.ui.btn_open_timming.y(), self.ui.btn_open_timming.width(), self.ui.btn_open_timming.height()))
        self.btn_animation.setEndValue(QRect(self.ui.btn_open_timming.x(), btn_end_y, self.ui.btn_open_timming.width(), self.ui.btn_open_timming.height()))
        self.btn_animation.start()

        self.ui.btn_open_timming.setText(btn_text)
        QTimer.singleShot(500, self.fixed)
        
    def fixed(self):
        if self.chose == "open":
            self.setMinimumHeight(690)
        else:
            self.setMaximumHeight(499)

    ###########################################################################

    ################ ФУНКЦИИ ДЛЯ АНИМЕ ############################################ 

    def start_work(self):
        try:
            if self.file_path_anime_pic is not None:
                if self.ui.check_post_site.isChecked():
                    self.ui.link_site.setText(unquote(self.ui.link_site.text()))
                    if not self.ui.link_site.text().startswith(os.getenv('CHECK_ANIMAUNT_LINK')) or self.ui.link_site.text() == '':
                        QMessageBox.warning(None, "Ошибка", "Ссылка на анимаунт указана не верно")
                        return
                    else:
                        self.link_site_animaunt = self.ui.link_site.text()
                if self.ui.check_malf_anime.isChecked():
                    if not self.ui.link_malfurik_anime.text().startswith(os.getenv('CHECK_MALFURIK_LINK')) or self.ui.link_malfurik_anime.text() == '':
                        QMessageBox.warning(None, "Ошибка", "Ссылка на малфурик указана не верно")
                        return
                    else:
                        self.link_malf_anime = self.ui.link_malfurik_anime.text()
                self.ui.btn_upload_anime.setEnabled(False)        
                self.ui.btn_pic_anime.setEnabled(False)        
                self.upload_manager.start_upload(self.file_path_anime_pic,
                                                self.file_path_anime_video,
                                                self.ui.check_sftp_anime.isChecked(),
                                                self.ui.check_malf_anime.isChecked(),
                                                self.ui.check_nonlink_anime.isChecked(),
                                                self.ui.check_post_site.isChecked(),
                                                self.link_site_animaunt,
                                                self.link_malf_anime,
                                                self.check_data, )
            else:
                QMessageBox.warning(None, "Ошибка", "Картинка не выбрана!")
        except Exception as e:
            self.file_path_anime_pic = None
            self.file_path_anime_video = None
            QMessageBox.warning(None, "Ошибка", f"Ошибка: {e}")
            
    def update_progress(self, value, mb_upload, mb_total, speed):
        self.ui.progress_anime.setValue(value)
        self.ui.progress_value.setText(f'Загружено: {mb_upload:.1f} МБ из {mb_total:.1f} МБ. Скорость: {speed:.1f} МБ/с')

    def upload_finished(self, result):
        name_folder = os.path.basename(os.path.dirname(self.file_path_anime_pic))
        self.ui.logging_upload.append(name_folder + " загружен в " + result)

    def upload_vk_finish(self, end):
        self.file_path_anime_pic = None 
        self.file_path_anime_video = None
        self.ui.btn_upload_anime.setDisabled(True)
        self.ui.check_malf_anime.setChecked(False)
        self.ui.check_nonlink_anime.setChecked(False)
        self.ui.check_post_site.setChecked(False)
        self.ui.check_sftp_anime.setChecked(False)
        self.ui.link_site.setText("")
        self.ui.link_malfurik_anime.setText("")
        self.ui.lbl_anime_pic.setText("Картинка не выбрана")
        self.ui.btn_video_anime.setText("Выбрать видео")
        self.ui.progress_value.setText("Загружено: 0 МБ из 0 МБ. Скорость: 0 МБ/с")
        self.ui.progress_anime.setValue(0)
        self.ui.dateEdit.setDate(QDate(self.year,  self.month, self.day))
        self.ui.btn_pic_anime.setEnabled(True)
        if end:
            self.ui.logging_upload.append("Запощено в вк!")
            self.ui.logging_upload.append("__________________________________\n")
        else:
            self.ui.logging_upload.append("Отмена загрузки.")
            self.ui.logging_upload.append("__________________________________\n")

    def select_picture_anime(self):
        self.picture_selector_anime.select_picture()

    def update_label_pic_anime(self, file_path):
        if file_path:
            file_name_without_extension, extension = os.path.splitext(os.path.basename(file_path))
            folder_name = os.path.basename(os.path.dirname(file_path))
            self.ui.lbl_anime_pic.setText(f"{folder_name} серия {file_name_without_extension}")
            self.file_path_anime_pic = file_path
            dbm = DatabaseManager()
            self.data = dbm.search_by_path_pic_anime(os.path.dirname(self.file_path_anime_pic))
            if not self.data:
                self.check_data = False
            else:
                self.check_data = True
                if self.data[0]["path_video"] == None or self.data[0]["path_video"] == "":
                    self.file_path_anime_video = None
                else:
                    search_number = str(file_name_without_extension.zfill(2))
                    search_pattern = os.path.join(self.data[0]["path_video"], f"{search_number}*.mp4")
                    try:
                        video_file = glob.glob(search_pattern)[0]
                        self.update_label_video_anime(video_file)
                    except:
                        video_file = None
                    

                self.ui.check_sftp_anime.setChecked(self.data[0]["check_sftp"])
                self.ui.check_nonlink_anime.setChecked(self.data[0]["check_nolink"])
                self.ui.check_malf_anime.setChecked(self.data[0]["check_malf"])
                self.ui.check_post_site.setChecked(self.data[0]["check_post_site"])
                self.ui.link_site.setText(self.data[0]["link_site"])
                self.ui.link_malfurik_anime.setText(self.data[0]["link_second_site"])
            self.ui.btn_upload_anime.setDisabled(False)
            if Config().get_id_chat():
                Dubbers().find_send_vk(path=file_path, main_window_ui=self)
        
    def select_video_anime(self):
        self.video_selector_anime.select_video()

    def update_label_video_anime(self, file_path):
        if file_path == "":
            self.file_path_anime_video = None
            self.ui.btn_video_anime.setText("Выбрать видео")
        else:
            file_name = os.path.basename(file_path)
            self.ui.btn_video_anime.setText(f"Серия {file_name}")
            self.file_path_anime_video = file_path

    def toggle_site_anime(self, state):
        if state == Qt.Checked:
            self.ui.link_malfurik_anime.setEnabled(True)
        else:
            self.ui.link_malfurik_anime.setEnabled(False)

    ##########################################################################

    ############################# ФУНКЦИИ ДЛЯ ДОРАМ ##########################

    def select_video_dorama(self):
        self.video_selector_dorama.select_video()

    def select_picture_dorama(self):
        self.pictute_selecor_dorama.select_picture()
        
    def update_video_dorama(self, file_path):
        if file_path:
            file_name_without_extension, extension = os.path.splitext(os.path.basename(file_path))
            folder_name = os.path.basename(os.path.dirname(file_path))
            self.ui.lbl_pic_video_dor.setText(f"{folder_name} серия {file_name_without_extension}")
            self.file_path_dorama_video = file_path
            dbm = DatabaseManager()
            self.data_dorama = dbm.search_by_path_video_dorama(os.path.dirname(self.file_path_dorama_video))
            if not self.data_dorama:
                self.check_data_dorama = False
            else:
                self.check_data_dorama = True
                if self.data_dorama[0]["path_pic"] == None or self.data_dorama[0]["path_pic"] == "":
                    self.file_path_dorama_pic = None
                else:
                    search_number = str(file_name_without_extension.zfill(2))
                    search_pattern = os.path.join(self.data[0]["path_pic"], f"{search_number}*.jpg")
                    try:
                        pic_file = glob.glob(search_pattern)[0]
                        self.update_picture_dorama(pic_file)
                    except:
                        pic_file = None
                self.ui.check_sftp_dor.setChecked(self.data_dorama[0]["check_sftp"])
                self.ui.check_tg_dor.setChecked(self.data_dorama[0]["check_telegram"])
                self.ui.check_vk_dor.setChecked(self.data_dorama[0]["check_vk"])
                self.ui.check_update_site_dor.setChecked(self.data_dorama[0]["check_site"])
                self.ui.line_link_animaunt_dor.setText(self.data_dorama[0]["link_second_site"])
                self.ui.line_link_malf_dor.setText(self.data_dorama[0]["link_site"])
            self.ui.btn_upload_dor.setDisabled(False)
            if Config().get_id_chat():
                Dubbers().find_send_vk(path=file_path, main_window_ui=self)
            self.timming_list = None
            all_item = self.ui.list_timming.findItems("", Qt.MatchContains)
            for item in all_item:
                item_data = item.data(Qt.UserRole)
                path_project = item_data.get("path_project")
                project_name = item_data.get("projectname")
                name_folder = os.path.basename(os.path.dirname(self.file_path_dorama_video))
                pattern = r'(\d+)(?=x\.mp4)'
                match = re.search(pattern, os.path.basename(self.file_path_dorama_video))
                if match:
                    number_project = match.group(1).lstrip('0')
                else:
                    number_project = None
                if name_folder in path_project:
                    if number_project in project_name:
                        self.ui.list_timming.setCurrentItem(item)
                        self.get_timming(item)
                        self.timming_list = timming.get_list(item_data)
                        break
            if self.timming_list is None:
                select_item = self.ui.list_timming.currentItem()
                if select_item is not None:
                    item_data = select_item.data(Qt.UserRole)
                    self.timming_list = timming.get_list(item_data)
                    if self.timming_list is None:
                        QMessageBox.warning(None, "Ошибка", "Не нашел тайминга")
    
    def update_picture_dorama(self, file_path):
        if file_path == "":
            self.file_path_dorama_pic = None
            self.ui.btn_chose_pic_dor.setText("Выбрать картинку")
        else:
            self.file_path_dorama_pic = file_path
            file_name = os.path.basename(file_path)
            self.ui.btn_chose_pic_dor.setText(file_name)
        
    def start_work_dorama(self):
        try:
            if self.ui.check_update_site_dor.isChecked():
                self.ui.line_link_animaunt_dor.setText(unquote(self.ui.line_link_animaunt_dor.text())) # Перекодируем текст если вдруг
                if not self.ui.line_link_malf_dor.text().startswith(os.getenv('CHECK_MALFURIK_LINK')) or self.ui.line_link_malf_dor.text() == '' or \
                        not self.ui.line_link_animaunt_dor.text().startswith(os.getenv('CHECK_ANIMAUNT_LINK')) or self.ui.line_link_animaunt_dor.text() == '':
                    QMessageBox.warning(None, "Ошибка", "Неверная ссылка на малфурик или анимаунт")
                    return
                if self.timming_list is None:
                    QMessageBox.warning(None, "Ошибка", "Не выбраны тайминги")
                    return
            self.ui.btn_upload_dor.setEnabled(False)
            self.ui.btn_chose_video_dor.setEnabled(False)
            self.upload_manager_dorama.start_upload(self.file_path_dorama_pic, self.file_path_dorama_video,
                                                    self.ui.check_sftp_dor.isChecked(), self.ui.check_vk_dor.isChecked(),
                                                    self.ui.check_tg_dor.isChecked(), self.ui.check_update_site_dor.isChecked(),
                                                    self.ui.line_link_animaunt_dor.text(), self.ui.line_link_malf_dor.text(),
                                                    self.check_data_dorama, self.timming_list)
        except Exception as e:
            QMessageBox.warning(None, "Ошибка", f"{e}")
            
    def update_progress_dor(self, value, mb_upload, mb_total, speed):
        self.ui.progressBar.setValue(value)
        self.ui.label_2.setText(f'Загружено: {mb_upload:.1f} МБ из {mb_total:.1f} МБ. Скорость: {speed:.1f} МБ/с')
        
    def finish_upload_sftp_dor(self, folder, time):
        self.ui.logging_upload.append(folder + " загружен в " + time)
        
    def finish_upload_tg_dor(self, finish):
        if finish:
            self.ui.logging_upload.append("Загружено в телеграмм")
        else:
            self.ui.logging_upload.append("Ошибка загрузки в телеграмм")
            
    def post_malf(self):
        select_item = self.ui.list_timming.currentItem()
        if select_item is not None:
            item_data = select_item.data(Qt.UserRole)
            timming_list = timming.get_list(item_data)
            if timming_list is not None:
                post = PostDorama().post_malfurik(timming_list)
                if post == True:
                    self.ui.logging_upload.append("На сайт было запощено")
                    self.ui.logging_upload.append("__________________________________\n")
                else:
                    QMessageBox.warning(None, "Ошибка", f"Произошла какая то ошибка\n{post}")
            else:
                QMessageBox.warning(None, "Ошибка", "Не правильно переданы тайминги")
        else:
            QMessageBox.warning(None, "Ошибка", "Тайминги не выбраны")
            
    def enable_timer_dor(self, state):
        if state == Qt.Checked:
            self.ui.check_timmer_dor.setEnabled(True)
        else:
            self.ui.check_timmer_dor.setChecked(False)
            self.ui.check_timmer_dor.setEnabled(False)
            
    def finish_dor(self):
        self.file_path_dorama_pic = None
        self.file_path_dorama_video = None
        self.ui.check_update_site_dor.setChecked(False)
        self.ui.btn_chose_pic_dor.setText("Выбрать картинку")
        self.ui.lbl_pic_video_dor.setText("Видео не выбрано")
        self.ui.progressBar.setValue(0)
        self.ui.label_2.setText("Загружено: 0 МБ из 0 МБ. Скорость: 0 МБ/с")
        self.ui.check_sftp_dor.setChecked(False)
        self.ui.check_tg_dor.setChecked(False)
        self.ui.check_vk_dor.setChecked(False)
        self.ui.check_update_site_dor.setChecked(False)
        self.ui.check_timmer_dor.setChecked(False)
        self.ui.check_timmer_dor.setEnabled(False)
        self.ui.btn_chose_video_dor.setEnabled(True)

    ##########################################################################

    ###########################  СДАЧА ДОРОГ #################################

    def save_id_chat(self, id):
        Config().set_id_chat(id)
        
    def btn_search_dub(self):
        Dubbers().find_send_vk(btn=True, main_window_ui=self)

    ########################################################################## 

    def center_screen(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_cyan.xml')
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
