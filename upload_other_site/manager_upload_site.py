from PyQt5.QtCore import QObject, Qt, pyqtSignal, QThread, QSize
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog
from upload_other_site.db_handler import DatabaseHandler
from upload_other_site.anime_up_other import AnimeUpOther
from upload_other_site.dorama_up_other import DoramaUpOther
from handle.parse_maunt import ParseMaunt
from handle.parse_malf import ParseMalf

import time
import re
import os
import log_config
import requests
from playwright.sync_api import sync_playwright
import threading
from bs4 import BeautifulSoup


class Dialog(QDialog):
    closed = pyqtSignal()

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Дополнительная информация')
        self.resize(QSize(300, 500))
        label1 = QLabel('Название:')
        self.lineedit1 = QLineEdit(self.name)
        self.lineedit1.setEnabled(False)
        label2 = QLabel('Ссылка Animaunt')
        self.lineedit2 = QLineEdit()
        label4 = QLabel('Ссылка на AnimeFind')
        self.lineedit4 = QLineEdit()
        label5 = QLabel('Ссылка на Anime365')
        self.lineedit5 = QLineEdit()
        label3 = QLabel('Путь:')
        self.lineedit3 = QLineEdit()
        self.lineedit3.setEnabled(False)
        button = QPushButton('Выбрать папку')
        button.clicked.connect(self.get_folder)
        button2 = QPushButton('Сохранить')
        button2.clicked.connect(self.save)

        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(self.lineedit1)
        layout.addWidget(label2)
        layout.addWidget(self.lineedit2)
        layout.addWidget(label4)
        layout.addWidget(self.lineedit4)
        layout.addWidget(label5)
        layout.addWidget(self.lineedit5)
        layout.addWidget(label3)
        layout.addWidget(self.lineedit3)
        layout.addWidget(button)
        layout.addWidget(button2)

        self.setLayout(layout)

    def get_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Выбрать папку')
        if folder:
            self.lineedit3.setText(folder)

    def save(self):
        self.closed.emit()
        self.accept()



class Signals(QObject):
    find_link = pyqtSignal(str, str)
    _365_link = pyqtSignal(str, str)

class UploadManagerOtherSite(QObject):

    def __init__(self, all_title):
        super().__init__()
        self.signals = Signals()
        self.worker = None
        self.all_title = all_title

    def run(self):
        try:
            titles_list = self.all_title.split('\n')
            data_list = [[title.rsplit(' ', 1)[0], title.rsplit(' ', 1)[1]] for title in titles_list if ' ' in title]
            for title in titles_list:
                words = title.split()
                if len(words) > 1:
                    name = ' '.join(words[:-1])
                    data = DatabaseHandler().get_data_by_name(name)
                    if data is None:
                        dialog = Dialog(name)
                        dialog.closed.connect(lambda: self.handle_dialog_close(dialog, name))
                        result = dialog.exec_()
                        if result == QDialog.Rejected:
                            return
            self.worker = ThreadUpload(data_list)
            # self.worker.setdata(data_list)
            self.worker.find_link.connect(self.signals.find_link)
            self.worker._365_link.connect(self.signals._365_link)
            self.worker.start()
            # self.worker.start()
            # thread = threading.Thread(target=ThreadUpload(data_list).run)
            # thread.start()
        except Exception as e:
            log_config.setup_logger().exception(e)

    def handle_dialog_close(self, dialog, name):
        name = dialog.lineedit1.text()
        animaunt_link = dialog.lineedit2.text()
        find_link = dialog.lineedit4.text()
        _365_link = dialog.lineedit5.text()
        path = dialog.lineedit3.text()
        DatabaseHandler().insert_data(name, animaunt_link, find_link, _365_link, path)
        dialog.deleteLater()

class ThreadUpload(QThread):
    find_link = pyqtSignal(str, str)
    _365_link = pyqtSignal(str, str)
    def __init__(self, data):
        super().__init__()
        self.data = data
        # self.data = data
        # self.anime_upload = AnimeUpOther()
        # self.anime_upload.find_anime.connect(self.find_link)
        # self.anime_upload._365_anime.connect(self._365_link)

    def setdata(self, data):
        self.data = data

    def run(self):
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            for item in self.data:
                name, episode = item[0], item[1]
                data_title = DatabaseHandler().get_data_by_name(name)
                find_seria = False
                code_file = ParseMaunt().get_list_series(data_title[2])
                for i in code_file:
                    if i[0] != '':
                        if i[1] == f'{episode} серия':
                            code_player = i[0]
                            file_name = i[0].split('/')[-1]
                            find_seria = True
                            break
                if find_seria:
                    if data_title[3] != '':
                        res_find, link_find = AnimeUpOther().findanime(data_title[3], code_player, episode)
                        if res_find == True:
                            self.find_link.emit("find", link_find)
                            pass
                        else:
                            self.find_link.emit("find",f"{link_find}")
                            pass
                    else:
                        self.find_link.emit("find", "Нет на сайте")
                        pass
                    if data_title[4] != '' and data_title[5] != '':
                        files = os.listdir(data_title[5])
                        if file_name in files:
                            file_path = os.path.join(data_title[5], file_name)
                            
                            res_365_, link_365_ = AnimeUpOther().anime365(data_title[4],
                                                                        episode, file_path, browser)
                            if res_365_ == True:
                                self._365_link.emit("365", link_365_)
                                pass
                            else:
                                self._365_link.emit("365", f"Ошибка, не нашел на сайте серию.{link_365_}")
                                pass
                        else:
                            self._365_link.emit("365", "Ошибка, не нашел файл в папке.")
                            pass
                    else:
                        self._365_link.emit("365", "Нет на сайте")
                        pass
                else:
                    self.find_link.emit("find", "Ошибка, не смог достать на маунте данные о серии.")
                    pass
                    self._365_link.emit("365", str(code_file))
                    pass


class DialogDorama(QDialog):
    closed = pyqtSignal()

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Дополнительная информация')
        self.resize(QSize(300, 300))
        label1 = QLabel('Название:')
        self.lineedit1 = QLineEdit(self.name)
        self.lineedit1.setEnabled(False)
        label2 = QLabel('Ссылка Malfurik')
        self.lineedit2 = QLineEdit()
        label4 = QLabel('Ссылка на DoramaTv')
        self.lineedit4 = QLineEdit()
        button2 = QPushButton('Сохранить')
        button2.clicked.connect(self.save)

        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(self.lineedit1)
        layout.addWidget(label2)
        layout.addWidget(self.lineedit2)
        layout.addWidget(label4)
        layout.addWidget(self.lineedit4)
        layout.addWidget(button2)

        self.setLayout(layout)

    def save(self):
        self.closed.emit()
        self.accept()


class ThreadUploadDorama(QThread):
    doramatv = pyqtSignal(str)

    def __init__(self, data):
        super().__init__()
        self.data = data

    def run(self):
        for item in self.data:
            name, episode = item[0], item[1]
            data_title = DatabaseHandler().get_data_by_name_dorama(name)
            links_video = ParseMalf().get_list_series(data_title[2])
            for link_video in links_video:
                if link_video[0] == f'{episode} серия':
                    req, doramatv_link = AnimeUpOther().findanime(data_title[3], link_video[1], episode, True)
                    # doramatv_link = DoramaUpOther().doramatv_uploader(data_title[3], episode, link_video)
                    if req:
                        self.doramatv.emit(doramatv_link)
                        break


class UploadManagerOtherDorama(QObject):
    doramatv = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.worker = None

    def start_upload(self, all_title):
        try:
            titles_list = all_title.split('\n')
            data_list = [[title.rsplit(' ', 1)[0], title.rsplit(' ', 1)[1]] for title in titles_list if ' ' in title]
            for title in titles_list:
                words = title.split()
                if len(words) > 1:
                    name = ' '.join(words[:-1])
                    data = DatabaseHandler().get_data_by_name_dorama(name)
                    if data is None:
                        dialog = DialogDorama(name)
                        dialog.closed.connect(lambda: self.handle_dialog_dorama_close(dialog, name))
                        result = dialog.exec_()
                        if result == QDialog.Rejected:
                            return
            self.worker = ThreadUploadDorama(data_list)
            self.worker.doramatv.connect(self.doramatv)
            self.worker.start()
        except Exception as e:
            log_config.setup_logger().exception(e)

    def handle_dialog_dorama_close(self, dialog, name):
        name = dialog.lineedit1.text()
        malfurik_link = dialog.lineedit2.text()
        doramatv_link = dialog.lineedit4.text()
        DatabaseHandler().insert_data_dorama(name, malfurik_link, doramatv_link)
        dialog.deleteLater()
