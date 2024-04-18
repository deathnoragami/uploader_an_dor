# pyinstaller --noconfirm --onedir --windowed --icon "D:\GitHub\Uploader/icon.ico" --name "AUPAn" --version-file "C:/Python/uploader_an_dor/version.txt" --add-data "C:/Python/uploader_an_dor/timming-e844f-firebase-adminsdk-s0m6j-53a96d672b.json;." --add-data "C:/Python/uploader_an_dor/.env;." --add-data "C:/Python/uploader_an_dor/icon.ico;." --add-data "C:/Python/uploader_an_dor/auto.png;."  "C:/Python/uploader_an_dor/app.py"
# pyinstaller --noconfirm --onedir --windowed --icon "D:/GitHub/Uploader/icon.ico" --name "AUPAn" --version-file "D:/GitHub/Uploader/version.txt" --add-data "D:/GitHub/Uploader/timming-e844f-firebase-adminsdk-s0m6j-53a96d672b.json;." --add-data "D:/GitHub/Uploader/.env;." --add-data "D:/GitHub/Uploader/icon.ico;." --add-data "D:/GitHub/Uploader/auto.png;." --add-data "D:/GitHub/Uploader/red.png;." --add-data "D:/GitHub/Uploader/green.png;." "D:/GitHub/Uploader/app.py"


# ! D:\GitHub\Uploader\venv\Scripts\python.exe

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon, QPainter, QColor, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem, QDateEdit, QWidget, \
    QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QDate, pyqtSignal, QThread
from ui import Ui_MainWindow
from ui_splash import Ui_SplashScreen

from Custom_Widgets.QCustomModals import QCustomModals

from autorization.autorization_application.autorizade_app import AuthorizationApp
from autorization.autorization_vk.autorizade_vk import AuthorizationVK
from autorization.autorization_tg.autorizade_tg import AuthorizationTG
from autorization.autorization_server.autorizade_sftp import AutorizationServer
from autorization.autorization_animaunt.autorization_web_animaunt import Animaunt_web
from autorization.autorization_malfurik.autorization_web_malfurik import Malfurik_web
from autorization.autorization_vk_site.autorization_web_vk import AutorizationWebVK
from autorization.checker_autorization import CheckerThread

from work_files.select_pic_anime import PictureSelectorAnime
from work_files.select_video_anime import VideoSelectorAnime
from work_files.select_video_dorama import VideoSelectorDorama
from work_files.select_pic_dorama import PictureSelectorDorama
from work_files.upload_anime import UploadManager
from work_files.upload_dorama import UploadManagerDorama
from work_files.post_dorama import PostDorama
from work_files.database_title import DataBase
from work_files.dubbers import Dubbers
from work_files.download_fix_timming import FixTimming
from work_files.version_checker import VersionChecker
from work_files.hentai_uploader import HentaiUploader

from upload_other_site.manager_upload_site import UploadManagerOtherSite

import timming_pro.timming_main as timming

from custom_widget.win_notify import notify
from config import Config
import win32api
import sys
import os
import glob
import json
import pytz
import datetime
import re
import resource_path
import log_config
import subprocess
import time
from urllib.parse import unquote
from dotenv import load_dotenv
import traceback

import qdarktheme
# from qt_material import apply_stylesheet
from postgre import Connect

load_dotenv(dotenv_path=resource_path.path(".env"))


class MasterThread(QThread):
    version_app = pyqtSignal(bool)
    auto_app = pyqtSignal(bool, bool, bool)

    def __init__(self, version, parent=None):
        super().__init__(parent)
        self.version = version

    def run(self):
        version_thread = VersionChecker(self.version)
        version_thread.check_version.connect(self.version_app)
        version_thread.start()
        version_thread.wait()

        site_thread = CheckerThread()
        site_thread.finished.connect(self.auto_app)
        site_thread.start()
        site_thread.wait()

class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)
        self.counter = 0
        self.setWindowIcon(QIcon(resource_path.path("icon.ico")))

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.progress_animation = QPropertyAnimation(self.ui.progressBar, b"value")
        self.progress_animation.setDuration(1000)
        self.progress_animation.setEasingCurve(QEasingCurve.Linear)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        try:
            info = win32api.GetFileVersionInfo("AUPAn.exe", '\\')
            major = info['FileVersionMS'] >> 16
            minor = info['FileVersionMS'] & 0xFFFF
            patch = info['FileVersionLS'] >> 16
            build = info['FileVersionLS'] & 0xFFFF
            self.version = f"{major}.{minor}.{patch}.{build}"
            self.setWindowTitle(f"AUPAn {self.version}")
        except win32api.error as e:
            self.version = '0.0.0.0'
            self.setWindowTitle(f"AUPAn")
        self.ui.label_description.setText("<strong>ПРОВЕРКА</strong> ВЕРСИИ")
        self.master_thread = MasterThread(self.version)
        self.master_thread.version_app.connect(self.handler_version_checker)
        self.master_thread.auto_app.connect(self.handler_site_checker)
        self.master_thread.start()
        self.show()

    def progress(self, count):
        current_value = self.ui.progressBar.value()
        self.progress_animation.setStartValue(current_value)
        self.progress_animation.setEndValue(count)
        self.progress_animation.start()
        if count == 60:
            self.progress_animation.finished.connect(self.end_open)

    def end_open(self):
        self.ui.label_description.setText("<strong>ШОКОЛАДКИ</strong> ДЕЛАЕМ")
        current_value = self.ui.progressBar.value()
        while current_value < 100:
            current_value += 1
            self.ui.progressBar.setValue(current_value)
            QtCore.QCoreApplication.processEvents()  # Обновляем пользовательский интерфейс
            time.sleep(0.04)  # Делаем небольшую паузу, чтобы не перегружать процессор
        main_window = MainWindow(self.version, self.malf_check, self.ani_check, self.vk_check)
        main_window.show()
        self.close()

    def handler_site_checker(self, malf_check, ani_check, vk_check):
        self.progress(60)
        self.malf_check = malf_check
        self.ani_check = ani_check
        self.vk_check = vk_check

    def handler_version_checker(self, check):
        if check:
            if os.path.exists("update.exe"):
                notify(title="Обновление",
                        msg="Вышло новое обновление программы, программа будет обновлена.")
                QApplication.quit()
                subprocess.Popen(["update.exe"])
            else:
                notify(title="Ошибка обновления",
                        msg="Не нашел файл обновления update.exe, скачайте его заново.")
                self.progress(20)
                self.ui.label_description.setText("<strong>ПРОВЕРКА</strong> АВТОРИЗАЦИЙ")
        else:
            self.progress(20)
            self.ui.label_description.setText("<strong>ПРОВЕРКА</strong> АВТОРИЗАЦИЙ")


class MainWindow(QMainWindow):
    other = pyqtSignal(bool)

    def __init__(self, version, malf_check, ani_check, vk_check):
        super(MainWindow, self).__init__()
        qdarktheme.setup_theme()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(f"AUPAn {version}")
        self.resize(1230, 600)


        # self.ui.frameTim.setMaximumHeight(0)
        # try:
        #     info = win32api.GetFileVersionInfo("AUPAn.exe", '\\')
        #     major = info['FileVersionMS'] >> 16
        #     minor = info['FileVersionMS'] & 0xFFFF
        #     patch = info['FileVersionLS'] >> 16
        #     build = info['FileVersionLS'] & 0xFFFF
        #     version = f"{major}.{minor}.{patch}.{build}"
        
        # except win32api.error as e:
        #     version = '0.0.0.0'
        #     self.setWindowTitle(f"AUPAn")

        # version_thread = VersionChecker(version=version)
        # version_thread.check_version.connect(self.handler_version_checker)
        # version_thread.start()

        # site_thread = CheckerThread()
        # site_thread.finished.connect(self.handler_site_checker)
        # site_thread.start()

        self.setWindowIcon(QIcon(resource_path.path("icon.ico")))
        # self.center_screen()

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
        self.ui.dateEdit.setDate(QDate(self.year, self.month, self.day))

        ########## ПРОВЕРКА АВТОРИЗАЦИИ ##################################

        user_autorization = False
        config = Config()
        uid = config.get_uid_program()
        if not uid == '':
            user_data = Connect().find_user_uid(uid)
            if user_data:
                user_autorization = True
                try:
                    self.ui.btn_navi_hentai.setEnabled(user_data[4])
                    self.ui.line_hentai_mail.setText(Config().get_email_hent())
                    self.ui.line_hentai_api.setText(Config().get_api_hent())
                except:
                    pass
                self.name_user = user_data[0]
                self.ui.menu_lbl_profile.setText(f"Профиль: {self.name_user}")
        else:
            user_data = False

        if not user_autorization:
            self.ui.menu_vk.setDisabled(True)
            self.ui.menu_tg.setDisabled(True)
            self.ui.menu_server.setDisabled(True)
            self.ui.menu_sait_animaunt.setDisabled(True)
            self.ui.menu_sait_malfurik.setDisabled(True)
            self.ui.menu_sait_vk.setDisabled(True)
            self.ui.stackedWidget.setCurrentIndex(1)
            self.ui.btn_navi_anime.setEnabled(False)
            self.ui.btn_navi_dorama.setEnabled(False)

        ##################################################################

        ########## Добавление чекбоксов дабберов #########################s####

        self.dub_data = Connect().get_dub_data()
        self.ui.scrollAreaWidgetContents.setLayout(QtWidgets.QVBoxLayout())
        # sorted_result = sorted(self.dub_data, key=lambda x: x['id'])
        self.checkbox_vars = []
        for item in self.dub_data:
            checkbox = QtWidgets.QCheckBox(item[0])  # Используем второй элемент кортежа как название чекбокса
            ping_value = item[2] # Проверяем наличие значения 'ping' и присваиваем, если есть
            self.checkbox_vars.append((checkbox, ping_value, item[0]))  # Добавляем кортеж в список checkbox_vars
            self.ui.scrollAreaWidgetContents.layout().addWidget(checkbox)

        #####################################################################

        ###################### АКТИВАЦИЯ ВИДЖЕТОВ ###########################
        if Config().get_vk_token() != "":
            self.ui.btn_pic_anime.setEnabled(True)
            self.ui.check_vk_dor.setEnabled(True)
            self.ui.check_novideo_dor.setEnabled(True)
            self.ui.line_search_dub_name_serial.setEnabled(True)
            self.ui.line_search_dub_number_serial.setEnabled(True)
            self.ui.line_prefix_name_serial.setEnabled(True)
            self.ui.btn_search_dubs.setEnabled(True)
        if os.path.exists("assets/my_session_tg.session"):
            self.ui.check_tg_dor.setEnabled(True)
        if user_data:
            maunt = Config().get_info_maunt()
            if maunt[0] != '' and maunt[1] != '':
                self.ui.check_sftp_anime.setEnabled(True)
            malf = Config().get_info_malf()
            if malf[0] != '' and malf[1] != '':
                self.ui.check_sftp_dor.setEnabled(True)
                # self.ui.btn_video_anime.setEnabled(True)
        if os.path.exists("assets/animaunt_storage.json"):
            self.ui.check_post_site.setEnabled(True)
            if os.path.exists("assets/malfurik_storage.json"):
                self.ui.check_update_site_dor.setEnabled(True)
        # if os.path.exists("assets/vk_storage.json"):
        #     self.ui.btn_chose_pic_dor.setEnabled(True)
        #####################################################################

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
        self.ui.textedit_timming_ad.mouseDoubleClickEvent = lambda event: self.copy(event, self.ui.textedit_timming_ad)
        self.ui.textedit_name_ad.mouseDoubleClickEvent = lambda event: self.copy(event, self.ui.textedit_name_ad)
        self.ui.btn_add_timming_malf.clicked.connect(self.post_malf)

        self.ui.logging_upload.mouseDoubleClickEvent = lambda event: self.copy_time(event, self.ui.logging_upload)

        ####################################### #############################

        ############# МЕНЮ  ####################################

        self.ui.menu_app.clicked.connect(AuthorizationApp)
        self.ui.menu_vk.clicked.connect(self.autorization_vk)
        self.ui.menu_tg.clicked.connect(self.autorization_tg)
        self.ui.menu_server.clicked.connect(self.autorization_sftp)

        self.ui.menu_sait_animaunt.clicked.connect(self.autorization_animaunt_web)
        self.ui.menu_sait_malfurik.clicked.connect(self.autorization_malfurik_web)
        self.ui.menu_sait_vk.clicked.connect(self.autorization_vk_web)

        self.ui.menu_fix_tim.clicked.connect(self.fix_timming)

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
        self.upload_manager.signals.finish_upload.connect(self.upload_finished)

        self.ui.check_malf_anime.stateChanged.connect(self.toggle_site_anime)

        #######################################################################

        ########################## ДОРАМЫ КНОПКИ ##############################

        self.video_selector_dorama = VideoSelectorDorama()
        self.video_selector_dorama.video_selected.connect(self.update_video_dorama)
        self.ui.btn_chose_video_dor.clicked.connect(self.select_video_dorama)

        self.pictute_selecor_dorama = PictureSelectorDorama()
        self.pictute_selecor_dorama.picture_selected.connect(self.update_picture_dorama)
        self.ui.btn_chose_pic_dor.clicked.connect(self.select_picture_dorama)

        # self.upload_manager_dorama = UploadManagerDorama(self)
        # self.upload_manager_dorama.signals.progress_changed.connect(self.update_progress_dor)
        # self.upload_manager_dorama.signals.finish_upload.connect(self.upload_finished_dor)

        self.ui.btn_upload_dor.clicked.connect(self.start_work_dorama)

        self.ui.check_update_site_dor.stateChanged.connect(self.enable_timer_dor)

        #######################################################################      

        ######################### СДАЧА ДОРОГ #################################

        self.ui.line_id_chat.setText(Config().get_id_chat())
        self.ui.line_id_chat.textChanged.connect(self.save_id_chat)
        self.ui.btn_search_dubs.clicked.connect(self.btn_search_dub)
        self.ui.text_send_dub.mouseDoubleClickEvent = lambda event: self.copy(event, self.ui.text_send_dub)

        self.ui.line_hentai_mail.textChanged.connect(self.save_email_hent)
        self.ui.line_hentai_api.textChanged.connect(self.save_api_hent)

        #######################################################################

        self.ui.pushButton_5.clicked.connect(self.slideleftMenu)
        self.ui.btn_navi_anime.clicked.connect(lambda: self.switch_chose(1, "upload"))
        self.ui.btn_navi_dorama.clicked.connect(lambda: self.switch_chose(0, "upload"))
        self.ui.btn_navi_autorization.clicked.connect(lambda: self.switch_chose(1, "setting"))
        self.ui.btn_navi_hentai.clicked.connect(lambda: self.switch_chose(2, "hentai"))
        self.ui.btn_navi_upload_other.clicked.connect(lambda: self.switch_chose(3, "upload_other"))

        self.ui.upload_hentai_del.clicked.connect(self.del_file_hent)
        self.ui.upload_hentai_del_all.clicked.connect(self.del_all_file_hent)

        green = QPixmap(resource_path.path("green.png"))
        red = QPixmap(resource_path.path("red.png"))
        if malf_check == True:
            self.ui.pixmap_malfurik.setPixmap(green)
        else:
            self.ui.pixmap_malfurik.setPixmap(red)
        if ani_check == True:
            self.ui.pixmap_animaunt.setPixmap(green)
        else:
            self.ui.pixmap_animaunt.setPixmap(red)
        if vk_check == True:
            self.ui.pixmap_vk.setPixmap(green)
        else:
            self.ui.pixmap_vk.setPixmap(red)

        self.setAcceptDrops(True)
        self.ui.upload_hentai.clicked.connect(self.hentai)

        
        self.ui.btn_anime_other_upload.clicked.connect(self.upload_other)
        self.ui.text_name_serial.mouseDoubleClickEvent = self.custom_paste
        self.manager_other = UploadManagerOtherSite()
        self.manager_other.find_link.connect(self.find_link)
        self.manager_other._365_link.connect(self.find_link)

    def custom_paste(self, event):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        lines = text.split('\n')
        formatted_lines = []
        for line in lines:
            parts = line.split()
            if len(parts) > 1:
                name = ' '.join(parts[:-1])
                episode_number = parts[-1]
                formatted_line = f"{name} {episode_number}\n"
                formatted_lines.append(formatted_line)
            else:
                formatted_lines.append(line + '\n')
        self.ui.text_name_serial.insertPlainText(''.join(formatted_lines))

    def upload_other(self):
        self.ui.text_link_find.clear()
        self.ui.text_link_365.clear()
        all_title = self.ui.text_name_serial.toPlainText()
        try:
            self.manager_other.start_upload(all_title)
        except Exception as e:
            log_config.setup_logger().exception(e)

    def find_link(self, site, link):
        if site == "find":
            self.ui.text_link_find.append(link)
        if site == "365":
            self.ui.text_link_365.append(link)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
                else:
                    links.append(str(url.toString()))
            self.ui.listWidget.addItems(links)
        else:
            event.ignore()

    def createIndicator(self, color):
        indicator = QWidget()
        indicator.setFixedSize(20, 20)

        # Переопределяем метод paintEvent для рисования кружка
        def paintEvent(event):
            painter = QPainter(indicator)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QColor(color))
            diameter = min(indicator.width(), indicator.height())
            center_x = (indicator.width() - diameter) // 2
            center_y = (indicator.height() - diameter) // 2
            painter.drawEllipse(center_x, center_y, diameter, diameter)

        indicator.paintEvent = paintEvent
        return indicator

    def switch_chose(self, index, page):
        if page == "upload":
            if index == 0:
                self.ui.chose_lbl_page.setText("Дорамы")
            else:
                self.ui.chose_lbl_page.setText("Аниме")
            self.ui.stackedWidget.setCurrentIndex(0)
            self.ui.stackedWidget_2.setCurrentIndex(index)
        elif page == "setting":
            self.ui.chose_lbl_page.setText("Авторизация")
            self.ui.stackedWidget.setCurrentIndex(index)
        elif page == "hentai":
            self.ui.chose_lbl_page.setText("Заливка хентая")
            self.ui.stackedWidget.setCurrentIndex(index)
        elif page == "upload_other":
            self.ui.chose_lbl_page.setText("Заливка")
            self.ui.stackedWidget.setCurrentIndex(index)

    def slideleftMenu(self):
        width = self.ui.leftMenuSlider.width()
        if width < 160:
            newWidth = 160
        else:
            newWidth = 60

        self.animation = QPropertyAnimation(self.ui.leftMenuSlider, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    ####################### ФУНКЦИИ ДЛЯ НАСТРОЕК ###########################

    def autorization_vk(self):
        check = AuthorizationVK()
        if check:
            self.ui.btn_pic_anime.setEnabled(True)
            self.ui.check_vk_dor.setEnabled(True)
            self.ui.check_novideo_dor.setEnabled(True)
            self.ui.line_search_dub_name_serial.setEnabled(True)
            self.ui.line_search_dub_number_serial.setEnabled(True)
            self.ui.line_prefix_name_serial.setEnabled(True)
            self.ui.btn_search_dubs.setEnabled(True)

    def autorization_tg(self):
        check = AuthorizationTG()
        if check:
            self.ui.check_tg_dor.setEnabled(True)

    def autorization_sftp(self):
        AutorizationServer()
        if all(item != '' for item in Config().get_info_malf()):
            self.ui.check_sftp_dor.setEnabled(True)
        if all(item != '' for item in Config().get_info_maunt()):
            self.ui.check_sftp_anime.setEnabled(True)

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
        # if os.path.exists("assets/vk_storage.json"):
        #     self.ui.btn_chose_pic_dor.setEnabled(True)

    def fix_timming(self):
        result, text = FixTimming().check_administration()
        if result:
            QMessageBox.information(self, "Информация", text)
        else:
            QMessageBox.warning(self, "Ошибка", text)

    ###########################################################################

    ##################### ФУНКЦИИ ДЛЯ ТАЙМИНГОВ ###############################

    def copy(self, event, ui_text):
        if event.button() == Qt.LeftButton:
            text = ui_text.toPlainText()
            if text:
                QApplication.clipboard().setText(f'"{text}"')

    def copy_time(self, event, ui_log):
        if event.button() == Qt.LeftButton:
            text = ui_log.toPlainText()
            if text:
                match = re.findall(r'сервер в (.+)', text)
                if match:
                    if len(match) > 1:
                        date_time = match[-1]
                    else:
                        date_time = match[0]
                    QApplication.clipboard().setText(date_time)

    def add_timming(self):
        data = timming.add_timming()
        if data == False:
            QMessageBox.warning(None, "Ошибка", "Премьер не запущен")
        else:
            item_text = f"{data['projectname']} Секв. {data['sequencename']}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, data)
            self.ui.list_timming.insertItem(0, item)
            self.get_timming(item)

    def get_timming(self, item):
        item_data = item.data(Qt.UserRole)
        self.times, self.name_ad = timming.format_timming(item_data)
        select_item = self.ui.list_timming.currentItem()
        if select_item is not None:
            item_data = select_item.data(Qt.UserRole)
            self.timming_list = timming.get_list(item_data)
        self.ui.textedit_timming_ad.setText(self.times)
        self.ui.textedit_name_ad.setText(self.name_ad)
        self.timming_list = timming.get_list(item_data)

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

    ###########################################################################

    ################ ФУНКЦИИ ДЛЯ АНИМЕ ############################################ 

    def start_work(self):
        try:
            if self.file_path_anime_pic is not None:
                if self.ui.check_post_site.isChecked():
                    self.ui.link_site.setText(unquote(self.ui.link_site.text()))
                    if not self.ui.link_site.text().startswith(
                            os.getenv('CHECK_ANIMAUNT_LINK')) or self.ui.link_site.text() == '':
                        QMessageBox.warning(None, "Ошибка", "Ссылка на анимаунт указана не верно")
                        return
                    else:
                        self.link_site_animaunt = self.ui.link_site.text()
                if self.ui.check_malf_anime.isChecked():
                    if not self.ui.link_malfurik_anime.text().startswith(
                            os.getenv('CHECK_MALFURIK_LINK')) or self.ui.link_malfurik_anime.text() == '':
                        QMessageBox.warning(None, "Ошибка", "Ссылка на малфурик указана не верно")
                        return
                    else:
                        self.link_malf_anime = self.ui.link_malfurik_anime.text()
                self.ui.btn_upload_anime.setEnabled(False)
                self.ui.btn_pic_anime.setEnabled(False)
                select_dub = Dubbers().select_checkboxes(self)
                self.upload_manager.start_upload(self.file_path_anime_pic,
                                                 self.file_path_anime_video,
                                                 self.ui.check_sftp_anime.isChecked(),
                                                 self.ui.check_malf_anime.isChecked(),
                                                 self.ui.check_nonlink_anime.isChecked(),
                                                 self.ui.check_post_site.isChecked(),
                                                 self.link_site_animaunt,
                                                 self.link_malf_anime,
                                                 select_dub)
            else:
                QMessageBox.warning(None, "Ошибка", "Картинка не выбрана!")
        except Exception as e:
            self.upload_finished(True, "Ошибка")
            log_config.logger.exception(e)

    def update_progress(self, value, mb_upload, mb_total, speed):
        self.ui.progress_anime.setValue(value)
        self.ui.progress_value.setText(
            f'Загружено: {mb_upload:.1f} МБ из {mb_total:.1f} МБ. Скорость: {speed:.1f} МБ/с')

    def upload_finished(self, end, text):
        self.ui.logging_upload.append(text)
        if end:
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
            self.ui.dateEdit.setDate(QDate(self.year, self.month, self.day))
            self.ui.btn_pic_anime.setEnabled(True)
            self.ui.btn_video_anime.setEnabled(False)
            self.ui.logging_upload.append('__________________________________\n')

    def select_picture_anime(self):
        try:
            self.picture_selector_anime.select_picture()
        except Exception as e:
            log_config.logger.exception(e)

    def update_label_pic_anime(self, file_path):
        if file_path:
            file_name_without_extension, extension = os.path.splitext(os.path.basename(file_path))
            folder_name = os.path.basename(os.path.dirname(file_path))
            self.ui.lbl_anime_pic.setText(f"{folder_name} серия {file_name_without_extension}")
            self.file_path_anime_pic = file_path
            with DataBase() as db:
                data = db.search_by_path_pic_anime(os.path.dirname(self.file_path_anime_pic))
                if data:
                    if data[0][2] == None or data[0][2] == "":
                        self.file_path_anime_video = None
                    else:
                        search_number = str(file_name_without_extension.zfill(2))
                        search_pattern = os.path.join(data[0][2], f"{search_number}*.mp4")
                        try:
                            video_file = glob.glob(search_pattern)[0]
                            self.update_label_video_anime(video_file)
                        except:
                            video_file = None
                    self.ui.check_sftp_anime.setChecked(data[0][4])
                    self.ui.check_nonlink_anime.setChecked(data[0][6])
                    self.ui.check_malf_anime.setChecked(data[0][5])
                    self.ui.check_post_site.setChecked(data[0][7])
                    self.ui.link_site.setText(data[0][8])
                    self.ui.link_malfurik_anime.setText(data[0][9])
                else:
                    self.file_path_anime_video = None
                    self.update_label_video_anime("")
                    self.ui.check_sftp_anime.setChecked(0)
                    self.ui.check_nonlink_anime.setChecked(0)
                    self.ui.check_malf_anime.setChecked(0)
                    self.ui.check_post_site.setChecked(0)
                    self.ui.link_site.setText("")
                    self.ui.link_malfurik_anime.setText("")
                self.ui.btn_upload_anime.setDisabled(False)
                if Config().get_id_chat():
                    Dubbers().find_send_vk(path=file_path, main_window_ui=self)
                self.ui.btn_video_anime.setEnabled(True)

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
            with DataBase() as db:
                data_dorama = db.search_by_path_video_dor(os.path.dirname(self.file_path_dorama_video))
            if data_dorama:
                if data_dorama[0][2] == None or data_dorama[0][2] == "":
                    self.file_path_dorama_pic = None
                else:
                    search_number = re.search(r'\d+', str(file_name_without_extension.zfill(2))).group()
                    search_pattern = os.path.join(data_dorama[0][2], f"{search_number}*.jpg")
                    try:
                        pic_file = glob.glob(search_pattern)[0]
                        self.update_picture_dorama(pic_file)
                    except Exception as e:
                        traceback.print_exc()
                        pic_file = None
                self.ui.check_sftp_dor.setChecked(data_dorama[0][4])
                self.ui.check_tg_dor.setChecked(data_dorama[0][6])
                self.ui.check_vk_dor.setChecked(data_dorama[0][5])
                self.ui.check_update_site_dor.setChecked(data_dorama[0][7])
                self.ui.line_link_malf_dor.setText(data_dorama[0][12])
                self.ui.line_link_animaunt_dor.setText(data_dorama[0][13])
            else:
                self.file_path_dorama_pic = None
                self.update_picture_dorama("")
                self.ui.check_sftp_dor.setChecked(0)
                self.ui.check_tg_dor.setChecked(0)
                self.ui.check_vk_dor.setChecked(0)
                self.ui.check_update_site_dor.setChecked(0)
                self.ui.line_link_malf_dor.setText("")
                self.ui.line_link_animaunt_dor.setText("")
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
            if os.path.exists("assets/vk_storage.json"):
                self.ui.btn_chose_pic_dor.setEnabled(True)
        else:
            self.file_path_dorama_video = None
            self.update_picture_dorama("")

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
                self.ui.line_link_animaunt_dor.setText(
                    unquote(self.ui.line_link_animaunt_dor.text()))  # Перекодируем текст если вдруг
                if not self.ui.line_link_malf_dor.text().startswith(
                        os.getenv('CHECK_MALFURIK_LINK')) or self.ui.line_link_malf_dor.text() == '' or \
                        not self.ui.line_link_animaunt_dor.text().startswith(
                            os.getenv('CHECK_ANIMAUNT_LINK')) or self.ui.line_link_animaunt_dor.text() == '':
                    QMessageBox.warning(None, "Ошибка", "Неверная ссылка на малфурик или анимаунт")
                    return
                if self.timming_list is None:
                    QMessageBox.warning(None, "Ошибка", "Не выбраны тайминги")
                    return
            select_dub = Dubbers().select_checkboxes(self)
            self.ui.btn_upload_dor.setEnabled(False)
            self.ui.btn_chose_video_dor.setEnabled(False)

            self.upload_manager_dorama = UploadManagerDorama(self, self.file_path_dorama_pic,
                                                             self.file_path_dorama_video,
                                                             self.ui.check_sftp_dor.isChecked(),
                                                             self.ui.check_vk_dor.isChecked(),
                                                             self.ui.check_tg_dor.isChecked(),
                                                             self.ui.check_update_site_dor.isChecked(),
                                                             self.ui.line_link_animaunt_dor.text(),
                                                             self.ui.line_link_malf_dor.text(),
                                                             self.timming_list, self.ui.check_novideo_dor.isChecked(),
                                                             select_dub)

            # self.upload_manager_dorama.start_upload()
            self.upload_manager_dorama.signals.progress_changed.connect(self.update_progress_dor)
            self.upload_manager_dorama.signals.finish_upload.connect(self.upload_finished_dor)
            self.upload_manager_dorama.signals.finish_sftp.connect(self.sftp_time)
            self.upload_manager_dorama.signals.ask.connect(self.ask)
            self.upload_manager_dorama.start()
        except Exception as e:
            QMessageBox.warning(None, "Ошибка", f"{e}")
            log_config.logger.exception(e)

    def sftp_time(self, text):
        self.ui.logging_upload.append(text)

    def ask(self, data, info, data_worker, update, update_values):
        if self.timming_list != None:
            list_tg = [self.name_user, self.name_ad]
        else: 
            list_tg = [self.name_user, "Не выбирал рекламу"]
        if update == False:
            title = f'VK плейлист - {info[1]}\n' \
                    f'VK пост - {info[2]}\n' \
                    f'TG пост - {info[0]}\n' \
                    f'Папка сервера - {info[3]}'
            q = QMessageBox.information(self, 'Информация', f"Проверьте данные\n{title}",
                                        QMessageBox.Yes | QMessageBox.No)
            if q == QMessageBox.Yes:
                self.upload_manager_dorama.signals.askk.emit(data, data_worker, update, update_values,
                                                             list_tg)
            else:
                self.upload_manager_dorama.exit()
        else:
            if not all(value is None for value in info):
                title = f'VK плейлист - {info[1]}\n' \
                        f'VK пост - {info[2]}\n' \
                        f'TG пост - {info[0]}\n' \
                        f'Папка сервера - {info[3]}'
                q = QMessageBox.information(self, 'Информация', f"Проверьте данные\n{title}",
                                            QMessageBox.Yes | QMessageBox.No)
                if q == QMessageBox.Yes:
                    self.upload_manager_dorama.signals.askk.emit(data, data_worker, update, update_values,
                                                                 list_tg)
                else:
                    self.upload_manager_dorama.exit()
            else:
                self.upload_manager_dorama.signals.askk.emit(data, data_worker, update, update_values,
                                                             list_tg)

    def post_malf(self):
        select_item = self.ui.list_timming.currentItem()
        if select_item is not None:
            if self.ui.line_add_timming_malf.text().startswith(
                    os.getenv('CHECK_MALFURIK_LINK')) or self.ui.line_add_timming_malf.text() != '':
                item_data = select_item.data(Qt.UserRole)
                timming_list = timming.get_list(item_data)
                if timming_list is not None:
                    post = PostDorama().post_malfurik(self.ui.line_add_timming_malf.text(), self.timming_list)
                    if post == True:
                        self.ui.logging_upload.append("На сайт было запощено")
                        self.ui.logging_upload.append("________________________________\n")
                    else:
                        QMessageBox.warning(None, "Ошибка", f"Произошла какая то ошибка\n{post}")
                else:
                    QMessageBox.warning(None, "Ошибка", "Не правильно переданы тайминги")
            else:
                QMessageBox.warning(None, "Ошибка", "Нет ссылки")
        else:
            QMessageBox.warning(None, "Ошибка", "Тайминги не выбраны")

    def enable_timer_dor(self, state):
        if state == Qt.Checked:
            self.ui.check_timmer_dor.setEnabled(True)
        else:
            self.ui.check_timmer_dor.setChecked(False)
            self.ui.check_timmer_dor.setEnabled(False)

    def update_progress_dor(self, value, mb_upload, mb_total, speed):
        self.ui.progressBar.setValue(value)
        self.ui.label_2.setText(f'Загружено: {mb_upload:.1f} МБ из {mb_total:.1f} МБ. Скорость: {speed:.1f} МБ/с')

    def upload_finished_dor(self, warning, name, upload):
        if upload == False:
            myModal = QCustomModals.InformationModal(
                title="Информация",
                parent=self,
                position='top-right',
                description=name + '\n', 
                isClosable=False,  
                animationDuration=2000 
            )
            myModal.show()
        else:
            self.ui.logging_upload.append(name)
        if warning:
            self.timming_list = None
            self.ui.logging_upload.append(name)
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
            self.ui.line_link_animaunt_dor.setText("")
            self.ui.line_link_malf_dor.setText("")
            self.ui.btn_chose_pic_dor.setEnabled(False)
            self.ui.logging_upload.append("________________________________\n")

    ##########################################################################

    ###########################  СДАЧА ДОРОГ #################################

    def save_id_chat(self, id):
        Config().set_id_chat(id)

    def btn_search_dub(self):
        if self.ui.line_search_dub_name_serial.text() and self.ui.line_search_dub_number_serial.text():
            Dubbers().find_send_vk(btn=True, main_window_ui=self)

    ########################################################################## 

    ########################## ХЕНТАЙ ########################################

    def save_email_hent(self, email):
        Config().set_email_hent(email)

    def save_api_hent(self, api):
        Config().set_api_hent(api)

    def hentai(self):
        all_item = []
        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            all_item.append(item.text())
        if all_item != []:
            self.work_hent = HentaiUploader(all_item, Config().get_api_hent(), Config().get_email_hent())
            self.work_hent.add_link.connect(self.add_link_hent)
            self.work_hent.start()

    def add_link_hent(self, link):
        last_line = self.ui.link_upload.toPlainText().split('\n')[-1]
        if last_line == "Загружаю...":
            cursor = self.ui.link_upload.textCursor()
            cursor.movePosition(cursor.End)
            cursor.select(cursor.BlockUnderCursor)
            cursor.removeSelectedText()
        self.ui.link_upload.append(link)

    def del_file_hent(self):
        selected_item = self.ui.listWidget.currentItem()
        if selected_item is not None:
            self.ui.listWidget.takeItem(self.ui.listWidget.row(selected_item))

    def del_all_file_hent(self):
        self.ui.listWidget.clear()
        self.ui.link_upload.clear()

    ##########################################################################

    def center_screen(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    # try:
    app = QApplication(sys.argv)
    # apply_stylesheet(app, theme='dark_cyan.xml')
    # qdarktheme.setup_theme()
    # main_window = MainWindow()
    # main_window.show()
    window = SplashScreen()
    sys.exit(app.exec_())
# except Exception as e:
#     log_config.setup_logger().exception(e)
