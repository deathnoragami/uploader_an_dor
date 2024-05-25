# pyinstaller --noconfirm --onedir --windowed --icon "C:/Python/Uploader/icon.ico" --name "AUPAn" --version-file "C:/Python/Uploader/version.txt" --add-data "C:/Python/Uploader/.env;." --add-data "C:/Python/Uploader/icon.ico;." --add-data "C:/Python/Uploader/logger_tg.session;." --add-data "C:/Python/Uploader/version.txt;." --add-data "C:/Python/Uploader/auto.png;."  "C:/Python/Uploader/app.py"
# pyinstaller --noconfirm --onedir --windowed --icon "D:/GitHub/Uploader/icon.ico" --name "AUPAn" --version-file "D:/GitHub/Uploader/version.txt" --add-data "D:/GitHub/Uploader/icon.ico;." --add-data "D:/GitHub/Uploader/.env;." --add-data "D:/GitHub/Uploader/logger_tg.session;."  --add-data "D:/GitHub/Uploader/auto.png;." --add-binary ".venv/Lib/site-packages/fake_useragent/data;fake_useragent/data"  "D:/GitHub/Uploader/app.py"


from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon, QPainter, QColor, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem, QDateEdit, QWidget, \
    QGraphicsDropShadowEffect, QDialog
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QDate, pyqtSignal, QThread, QPoint
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
from autorization.autorization_findanime.autorization_find import AnimeFind_Web
from autorization.autorization_smotret_anime.autorization_365_smotret import _365_Web
from autorization.autorization_sites.autorization_sites import AutorizationSites

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

from handle.parse_malf import ParseMalf
from handle.parse_maunt import ParseMaunt

from hurdsub_worker.hurdsub import WorkerHardSub

from upload_other_site.manager_upload_site import UploadManagerOtherSite, UploadManagerOtherDorama

import timming_pro.timming_main as timming
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
import requests
from bs4 import BeautifulSoup

import qdarktheme
from qt_material import apply_stylesheet
from postgre import Connect

load_dotenv(dotenv_path=resource_path.path(".env"))



class MainWindow(QMainWindow):
    other = pyqtSignal(bool)

    def __init__(self):
        super(MainWindow, self).__init__()
        # apply_stylesheet(app, theme="dark_cyan.xml")
        # qdarktheme.setup_theme(theme="auto")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.resize(1200, 625)
        self.ui.dateEdit.setButtonSymbols(QDateEdit.NoButtons)

        # ВСЕ ДЛЯ СТАТУС БАРА
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.ui.minimize_btn.clicked.connect(self.showMinimized)
        self.ui.close_btn.clicked.connect(self.close)

        self.old_pos = self.pos()
        self.mouse_pressed = False
        try:
            info = win32api.GetFileVersionInfo("AUPAn.exe", '\\')
            major = info['FileVersionMS'] >> 16
            minor = info['FileVersionMS'] & 0xFFFF
            patch = info['FileVersionLS'] >> 16
            build = info['FileVersionLS'] & 0xFFFF
            version = f"{major}.{minor}.{patch}.{build}"
            self.setWindowTitle(f"AUPAn {version}")
        except win32api.error as e:
            version = '0.0.0.0'
            self.setWindowTitle(f"AUPAn")

        version_thread = VersionChecker(version=version)
        version_thread.start()

        site_thread = CheckerThread()
        site_thread.finished.connect(self.pix_map_login)
        site_thread.start()

        self.setWindowIcon(QIcon(resource_path.path("icon.ico")))
        # self.center_screen()

        ############## ОБНУЛЕНИЕ ПЕРЕМЕННЫХ #############################

        self.file_path_anime_pic = None
        self.file_path_anime_video = None
        self.file_path_dorama_pic = None
        self.file_path_dorama_video = None
        self.link_site_animaunt = None
        self.link_malf_anime = None
        self.timming_list = None

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
            self.ui.menu_login_sites.setDisabled(True)
            self.ui.menu_sait_vk.setDisabled(True)
            self.ui.stackedWidget.setCurrentIndex(1)
            self.ui.btn_navi_anime.setEnabled(False)
            self.ui.btn_navi_dorama.setEnabled(False)
            self.ui.combobox_find_ad.setEnabled(False)

        ##################################################################

        ########## Добавление чекбоксов дабберов #########################s####

        self.dub_data = Connect().get_dub_data()
        self.ui.scrollAreaWidgetContents.setLayout(QtWidgets.QVBoxLayout())
        # sorted_result = sorted(self.dub_data, key=lambda x: x['id'])
        self.checkbox_vars = []
        for item in self.dub_data:
            checkbox = QtWidgets.QCheckBox(item[0])  # Используем второй элемент кортежа как название чекбокса
            ping_value = item[2]  # Проверяем наличие значения 'ping' и присваиваем, если есть
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
        # if os.path.exists("assets/animaunt_storage.json"):
        #     self.ui.check_post_site.setEnabled(True)
        #     if os.path.exists("assets/malfurik_storage.json"):
        #         self.ui.check_update_site_dor.setEnabled(True)
        #         if os.path.exists("assets/findanime_storage.json"):
        #             self.ui.btn_dorama_other_upload.setEnabled(True)
        #     if os.path.exists("assets/findanime_storage.json"):
        

        # if os.path.exists("assets/vk_storage.json"):
        #     self.ui.btn_chose_pic_dor.setEnabled(True)
        #####################################################################
        if Config().get_a_info_site()[0] != '' and Config().get_a_info_site()[1] != '':
            self.ui.check_post_site.setEnabled(True)
            if os.path.exists("assets/anime365_storage.json"):
                self.ui.btn_anime_other_upload.setEnabled(True)
        if Config().get_m_info_site()[0] != '' and Config().get_m_info_site()[1] != '':
            self.ui.check_update_site_dor.setEnabled(True)
            self.ui.btn_dorama_other_upload.setEnabled(True)
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

        self.ui.menu_login_sites.clicked.connect(self.autorization_all_sites)
        self.ui.menu_sait_vk.clicked.connect(self.autorization_vk_web)
        self.ui.menu_sait_365.clicked.connect(self.autorization_365_web)

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
        self.ui.btn_navi_upload_other.clicked.connect(lambda: self.switch_upload_other())
        self.ui.btn_other_upload_dorama.clicked.connect(lambda: self.switch_upload_other("dorama"))
        self.ui.btn_other_upload_anime.clicked.connect(lambda: self.switch_upload_other("anime"))

        self.ui.upload_hentai_del.clicked.connect(self.del_file_hent)
        self.ui.upload_hentai_del_all.clicked.connect(self.del_all_file_hent)

        self.setAcceptDrops(True)
        self.ui.upload_hentai.clicked.connect(self.hentai)

        self.ui.btn_anime_other_upload.clicked.connect(self.upload_other)
        self.ui.btn_dorama_other_upload.clicked.connect(self.upload_other_dorama)
        self.ui.text_name_serial.mouseDoubleClickEvent = self.custom_paste
        self.ui.text_link_malfurik.mouseDoubleClickEvent = self.custom_paste_dorama

        self.manager_other_dorama = UploadManagerOtherDorama()
        self.manager_other_dorama.doramatv.connect(self.doramatv_link)

        serial_names = [row[0] for row in Connect().get_all_serials()]
        self.ui.combobox_find_ad.addItems(serial_names)
        self.ui.combobox_find_ad.activated.connect(self.combo)
        

        self.ui.btn_start_hardsub.clicked.connect(self.start_hardsub)


    # ПЕРЕДВИЖЕНИЕ ПРОГРАММЫ ПО СТАТУС БАРУ
    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()
        self.mouse_pressed = True

    def mouseMoveEvent(self, event):
        if self.mouse_pressed:
            delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.mouse_pressed = False

    def combo(self):
        text = self.ui.combobox_find_ad.currentText()
        text = Connect().search_ad_without_number(text)
        formatted_string = "{} серия {}\n{}".format(text[0], text[1] + "\n", "\n".join(text[2].split('\r\n')))
        Modal = QCustomModals.SuccessModal(
            title="Реклама",
            parent=self,
            position='top-left',
            description=formatted_string,
            isClosable=True,
            animationDuration=30000
        )
        Modal.show()

    def search_last_ad(self, name_sftp, number):
        parts = name_sftp.split("]")
        if len(parts) > 1:
            name_sftp = parts[1].strip()
            if "|" in name_sftp:
                name_sftp = name_sftp.split("|")[0].strip()
        text = Connect().search_ad_without_number(name_sftp)
        if text:
            if int(text[1]) == int(number) - 1:
                list_search_ad = [item.strip() for item in text[2].split('\n') if
                                  item.strip() and "Начитка" not in item]
                text_ad = self.ui.textedit_name_ad.toPlainText()
                list_current_ad = [item.strip() for item in text_ad.split('\n') if
                                   item.strip() and "Начитка" not in item]
                overlap_ad = []
                for item1, item2 in zip(list_search_ad, list_current_ad):
                    if item1 == item2:
                        overlap_ad.append(item1)
                if overlap_ad:
                    return [text[0], text[1], overlap_ad]
                else:
                    return None
            else:
                myModal = QCustomModals.WarningModal(
                    title="Реклама",
                    parent=self,
                    position='top-left',
                    description=f"Нет прошлой серии\nРеклама {text[0]} {text[1]}\n\n{text[2]}",
                    isClosable=True,
                    animationDuration=10000
                )
                myModal.show()
                return None
        else:
            myModal = QCustomModals.ErrorModal(
                title="Реклама",
                parent=self,
                position='top-left',
                description=f"В Базе пока нет этого релиза. Ты первопроходец =)",
                isClosable=True,
                animationDuration=5000
            )
            myModal.show()
            return None

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

    def custom_paste_dorama(self, event):
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
        self.ui.text_link_malfurik.insertPlainText(''.join(formatted_lines))

    def upload_other(self):
        self.ui.text_link_find.clear()
        self.ui.text_link_365.clear()
        all_title = self.ui.text_name_serial.toPlainText()
        try:
            self.manager_other = UploadManagerOtherSite(all_title)
            self.manager_other.signals.find_link.connect(self.find_link)
            self.manager_other.signals._365_link.connect(self.find_link)
            self.manager_other.run()
        except Exception as e:
            log_config.setup_logger().exception(e)

    def upload_other_dorama(self):
        self.ui.text_link_doramatv.clear()
        all_title = self.ui.text_link_malfurik.toPlainText()
        try:
            self.manager_other_dorama.start_upload(all_title)
        except Exception as e:
            log_config.setup_logger().exception(e)

    def find_link(self, site, link):
        if site == "find":
            self.ui.text_link_find.append(link)
        if site == "365":
            self.ui.text_link_365.append(link)

    def doramatv_link(self, link):
        self.ui.text_link_doramatv.append(link)

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

    def switch_upload_other(self, page=None):
        self.ui.stackedWidget.setCurrentIndex(4)
        if page == "anime":
            self.ui.chose_lbl_page.setText("Заливка аниме")
            self.ui.stackedWidget_3.setCurrentIndex(0)
        elif page == "dorama":
            self.ui.chose_lbl_page.setText("Заливка дорам")
            self.ui.stackedWidget_3.setCurrentIndex(1)
        else:
            if self.ui.stackedWidget_3.currentIndex() == 0:
                self.ui.chose_lbl_page.setText("Заливка аниме")
            else:
                self.ui.chose_lbl_page.setText("Заливка дорам")

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

    def pix_map_login(self, auth):
        if auth == True:
            self.ui.checker_vk.setStyleSheet("color: green;")
        else:
            self.ui.checker_vk.setStyleSheet("color: red;")

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

    def autorization_all_sites(self):
        AutorizationSites()
        if Config().get_a_info_site()[0] != '' and Config().get_a_info_site()[1] != '':
            self.ui.check_post_site.setEnabled(True)
            if os.path.exists("assets/anime365_storage.json"):
                self.ui.btn_anime_other_upload.setEnabled(True)
        if Config().get_m_info_site()[0] != '' and Config().get_m_info_site()[1] != '':
            self.ui.check_update_site_dor.setEnabled(True)
            self.ui.btn_dorama_other_upload.setEnabled(True)
        ################## ТАЙМИНГ ############################
        # ParseMaunt().update_seria_maunt(r'https://animaunt.org/%E7%A7%81%E3%81%AF%E7%8B%AC%E8%BA%AB%E3%81%A7%E3%81%99.php?mod=editnews&action=editnews&id=13966', 
        #                                 '31', dorama=True, timer=True)


    def autorization_vk_web(self):
        AutorizationWebVK()
        if os.path.exists("assets/vk_storage.json"):
            self.ui.pixmap_vk.setPixmap(self.green)

    def autorization_365_web(self):
        res = _365_Web().autorization()
        if res:
            QMessageBox.information(self, "Авторизация", "Авторизация успешна")
        else:
            QMessageBox.warning(self, "Авторизация", "Ошибка при авторизации.")
        if os.path.exists("assets/animaunt_storage.json") and os.path.exists(
                "assets/anime365_storage.json") and os.path.exists("assets/findanime_storage.json"):
            self.ui.btn_anime_other_upload.setEnabled(True)

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
            item.setSelected(True)
            self.get_timming(item)
            item_data = item.data(Qt.UserRole)
            self.timming_list = timming.get_list(item_data)

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
                    self.ui.textedit_name_ad.clear()
                    self.ui.textedit_timming_ad.clear()

    ###########################################################################

    ################ ФУНКЦИИ ДЛЯ АНИМЕ ############################################ 

    def start_work(self):
        try:
            if self.file_path_anime_pic is not None:
                if self.ui.check_post_site.isChecked():
                    self.ui.link_site.setText(unquote(self.ui.link_site.text()))
                    if self.ui.link_site.text() == '':
                        QMessageBox.warning(None, "Ошибка", "Ссылка на сайт не указана")
                    elif self.ui.link_site.text().startswith(os.getenv('CHECK_ANIMAUNT_LINK')):
                        self.link_site_animaunt = self.ui.link_site.text()
                    elif self.ui.link_site.text().startswith('https://animaunt.org/'):
                        match = re.search(r'(\d+)-', self.ui.link_site.text()).group(1)
                        self.link_site_animaunt = os.getenv('CHECK_ANIMAUNT_LINK') + '&action=editnews&id=' + match
                    else:
                        QMessageBox.warning(None, "Ошибка", "Ссылка на сайт указана не верно")
                        return
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
                                                 select_dub,
                                                 self.name_user)
            else:
                QMessageBox.warning(self, "Ошибка", "Картинка не выбрана!")
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
                    if self.ui.check_sftp_anime.isEnabled():
                        self.ui.check_sftp_anime.setChecked(data[0][4])
                    self.ui.check_nonlink_anime.setChecked(data[0][6])
                    self.ui.check_malf_anime.setChecked(data[0][5])
                    if self.ui.check_post_site.isEnabled():
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
                self.data_dorama = db.search_by_path_video_dor(os.path.dirname(self.file_path_dorama_video))
            if self.data_dorama:
                if self.data_dorama[0][2] == None or self.data_dorama[0][2] == "":
                    self.file_path_dorama_pic = None
                else:
                    search_number = re.search(r'\d+', str(file_name_without_extension.zfill(2))).group()
                    search_pattern = os.path.join(self.data_dorama[0][2], f"{search_number}*.jpg")
                    try:
                        pic_file = glob.glob(search_pattern)[0]
                        self.update_picture_dorama(pic_file)
                    except Exception as e:
                        traceback.print_exc()
                if self.ui.check_sftp_dor.isEnabled():
                    self.ui.check_sftp_dor.setChecked(self.data_dorama[0][4])
                if self.ui.check_tg_dor.isEnabled():
                    self.ui.check_tg_dor.setChecked(self.data_dorama[0][6])
                if self.ui.check_vk_dor.isEnabled():
                    self.ui.check_vk_dor.setChecked(self.data_dorama[0][5])
                if self.ui.check_update_site_dor.isEnabled():
                    self.ui.check_update_site_dor.setChecked(self.data_dorama[0][7])
                    self.ui.line_link_malf_dor.setText(self.data_dorama[0][12])
                    self.ui.line_link_animaunt_dor.setText(self.data_dorama[0][13])
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
                        item.setSelected(True)
                        self.get_timming(item)
                        self.timming_list = timming.get_list(item_data)
                        break
            if self.timming_list == None:
                self.ui.textedit_name_ad.clear()
                self.ui.textedit_timming_ad.clear()
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
                self.ui.line_link_animaunt_dor.setText(unquote(self.ui.line_link_animaunt_dor.text()))  # Перекодируем текст если вдруг
                if self.ui.line_link_animaunt_dor.text() == '':
                    QMessageBox.warning(self, "Ошибка", "Ссылка на анимаунт не указана")
                elif self.ui.line_link_animaunt_dor.text().startswith(os.getenv('CHECK_ANIMAUNT_LINK')):
                    self.link_site_animaunt = self.ui.line_link_animaunt_dor.text()
                elif self.ui.line_link_animaunt_dor.text().startswith('https://animaunt.org/'):
                    match = re.search(r'(\d+)-', self.ui.line_link_animaunt_dor.text()).group(1)
                    self.link_site_animaunt = os.getenv('CHECK_ANIMAUNT_LINK') + '&action=editnews&id=' + match
                else:
                    QMessageBox.warning(self, "Ошибка", "Ссылка на анимаунт указана не верно")
                
                if self.ui.line_link_malf_dor.text() == '':
                    QMessageBox.warning(self, "Ошибка", "Ссылка на малфурик не указана")
                elif self.ui.line_link_malf_dor.text().startswith(os.getenv('CHECK_MALFURIK_LINK')):
                    self.link_site_malfurik = self.ui.line_link_malf_dor.text()
                elif self.ui.line_link_malf_dor.text().startswith('https://anime.malfurik.online'):
                    response = requests.get(self.ui.line_link_malf_dor.text())
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        link_tag = soup.find('link', rel='shortlink')
                        if link_tag:
                            href = link_tag.get('href')
                            match = re.search(r'\?p=(\d+)', href)
                            number = match.group(1)
                            self.link_site_malfurik = f"https://anime.malfurik.online/wp-admin/post.php?post={number}&action=edit"
                else:
                    QMessageBox.warning(self, "Ошибка", "Ссылка на малфурик указана не верно")
            else:
                self.link_site_malfurik = None
                self.link_site_animaunt = None
            select_dub = Dubbers().select_checkboxes(self)
            self.ui.btn_upload_dor.setEnabled(False)
            self.ui.btn_chose_video_dor.setEnabled(False)
            self.ui.btn_chose_pic_dor.setEnabled(False)
            if self.data_dorama:
                if self.data_dorama[0][3] != '':
                    name_file = os.path.splitext(os.path.basename(self.file_path_dorama_video))[0].lstrip('0').replace(
                        'x', '')
                    overlap_ad = self.search_last_ad(self.data_dorama[0][3], name_file)
                    if overlap_ad:
                        q = QMessageBox.warning(self, "Реклама",
                                                f"У вас есть повторяющаяся реклама с прошлой серией\n" \
                                                f"{overlap_ad[0]} {overlap_ad[1]} {overlap_ad[2]}\n" \
                                                f"Вы точно хотите продолжить загрузку?",
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if q == QMessageBox.No:
                            text = f"Загрузка {self.data_dorama[0][3]} {name_file} прервана."
                            self.upload_finished_dor(True, text, True)
                            return
            self.upload_manager_dorama = UploadManagerDorama(self, self.file_path_dorama_pic,
                                                             self.file_path_dorama_video,
                                                             self.ui.check_sftp_dor.isChecked(),
                                                             self.ui.check_vk_dor.isChecked(),
                                                             self.ui.check_tg_dor.isChecked(),
                                                             self.ui.check_update_site_dor.isChecked(),
                                                             self.link_site_animaunt,
                                                             self.link_site_malfurik,
                                                             self.timming_list, self.ui.check_novideo_dor.isChecked(),
                                                             select_dub)
            self.upload_manager_dorama.signals.progress_changed.connect(self.update_progress_dor)
            self.upload_manager_dorama.signals.finish_upload.connect(self.upload_finished_dor)
            self.upload_manager_dorama.signals.finish_sftp.connect(self.sftp_time)
            self.upload_manager_dorama.signals.ask.connect(self.ask)
            self.upload_manager_dorama.start()
        except Exception as e:
            QMessageBox.warning(None, "Ошибка", f"{e}")
            log_config.setup_logger().exception(e)

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
        if self.timming_list is not None:
            if self.ui.line_add_timming_malf.text().startswith(
                    os.getenv('CHECK_MALFURIK_LINK')) or self.ui.line_add_timming_malf.text() != '':
                item_data = select_item.data(Qt.UserRole)
                timming_list = timming.get_list(item_data)
                if timming_list is not None:
                    # self.only_post = ParseMalf()
                    # self.only_post.update_seria_malf(self.ui.line_add_timming_malf.text(), self.timming_list)
                    # self.only_post.start()
                    post = ParseMalf().update_seria_malf(self.ui.line_add_timming_malf.text(), self.timming_list)
                    # post = PostDorama().post_malfurik(self.ui.line_add_timming_malf.text(), self.timming_list)
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
            self.ui.logging_upload.append("________________________________\n")

    ##########################################################################

    ###########################  ХАРД САБ  #################################

    def start_hardsub(self):
        path = r'D:/Work/Аниме/Лунное путешествие приведёт к новому миру 2/19/19.mkv'
        self.hardsub_worker = WorkerHardSub(self, path)
        self.hardsub_worker.start()

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
    try:
        app = QApplication(sys.argv)
        # apply_stylesheet(app, theme='dark_cyan.xml')
        # qdarktheme.setup_theme()
        main_window = MainWindow()
        main_window.show()

        # main_window = MainWindow('0.0.0.0', True, True, True)
        # main_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        log_config.setup_logger().exception(e)
