from PyQt5.QtCore import QObject, Qt, pyqtSignal, QThread, QSize
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog
from upload_other_site.db_handler import DatabaseHandler
from upload_other_site.anime_up_other import AnimeUpOther
from upload_other_site.dorama_up_other import DoramaUpOther

import re
import os
import log_config
import requests

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


class ThreadUpload(QThread):
    find_link = pyqtSignal(str, str)
    _365_link = pyqtSignal(str, str)

    def setdata(self, data):
        self.data = data

    def run(self):
        for item in self.data:
            name, episode = item[0], item[1]
            data_title = DatabaseHandler().get_data_by_name(name)
            res, code_file = AnimeUpOther().animaunt_checker(data_title[2], episode)
            if res == True:
                code_player = code_file[0]
                file_name = code_file[1]
                if data_title[3] != '':
                    res_find, link_find = AnimeUpOther().findanime(data_title[3], episode,
                                                                   code_player)
                    if res_find == True:
                        self.find_link.emit("find", link_find)
                    else:
                        self.find_link.emit("find", "Ошибка, не нашел на сайте серию.")
                else:
                    self.find_link.emit("find", "Нет на сайте")
                if data_title[4] != '' and data_title[5] != '':
                    files = os.listdir(data_title[5])
                    if file_name in files:
                        file_path = os.path.join(data_title[5], file_name)
                        res_365_, link_365_ = AnimeUpOther().anime365(data_title[4],
                                                                      episode, file_path)
                        if res_365_ == True:
                            self._365_link.emit("365", link_365_)
                        else:
                            self._365_link.emit("365", "Ошибка, не нашел на сайте серию.")
                    else:
                        self._365_link.emit("365", "Ошибка, не нашел файл в папке.")
                else:
                    self._365_link.emit("365", "Нет на сайте")
            else:
                self.find_link.emit("find", "Ошибка, не смог достать на маунте данные о серии.")
                self._365_link.emit("365", str(code_file))


class UploadManagerOtherSite(QObject):
    find_link = pyqtSignal(str, str)
    _365_link = pyqtSignal(str, str)

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
                    data = DatabaseHandler().get_data_by_name(name)
                    if data is None:
                        dialog = Dialog(name)
                        dialog.closed.connect(lambda: self.handle_dialog_close(dialog, name))
                        result = dialog.exec_()
                        if result == QDialog.Rejected:
                            return
            self.worker = ThreadUpload()
            self.worker.setdata(data_list)
            self.worker.find_link.connect(self.find_link)
            self.worker._365_link.connect(self._365_link)
            self.worker.start()
            # threading.Thread(target=ThreadUpload, args=(data_list, self.ui)).start()
        except Exception as e:
            log_config.setup_logger().exception(e)

    def handle_dialog_close(self, dialog, name):
        name = dialog.lineedit1.text()
        animaunt_link = dialog.lineedit2.text()
        match = re.search(r'/(\d+)-', animaunt_link)
        animaunt_link = os.getenv("CHECK_ANIMAUNT_LINK") + "&action=editnews&id=" + match.group(1)
        find_link = dialog.lineedit4.text()
        _365_link = dialog.lineedit5.text()
        path = dialog.lineedit3.text()
        DatabaseHandler().insert_data(name, animaunt_link, find_link, _365_link, path)
        dialog.deleteLater()


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
            link_video = DoramaUpOther().malfurik_checker(data_title[2], episode)
            if link_video:
                doramatv_link = DoramaUpOther().doramatv_uploader(data_title[3], episode, link_video)
                if doramatv_link:
                    self.doramatv.emit(doramatv_link)


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
        response = requests.get(malfurik_link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            link_tag = soup.find('link', rel='shortlink')
            if link_tag:
                href = link_tag.get('href')
                match = re.search(r'\?p=(\d+)', href)
                number = match.group(1)
        malfurik_link = f"https://anime.malfurik.online/wp-admin/post.php?post={number}&action=edit"
        doramatv_link = dialog.lineedit4.text()
        DatabaseHandler().insert_data_dorama(name, malfurik_link, doramatv_link)
        dialog.deleteLater()
