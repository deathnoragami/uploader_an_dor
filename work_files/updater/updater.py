# pyinstaller --noconfirm --onefile --windowed --icon "C:/Python/uploader_an_dor/work_files/updater/update_icon.ico" --name "update" --add-data "C:/Python/uploader_an_dor/work_files/updater/right_pic.gif;." --add-data "C:/Python/uploader_an_dor/work_files/updater/update_icon.ico;."  "C:/Python/uploader_an_dor/work_files/updater/updater.py"
# pyinstaller --noconfirm --onefile --windowed --icon "D:/GitHub/Uploader/work_files/updater/update_icon.ico" --name "update" --add-data "D:/GitHub/Uploader/work_files/updater/right_pic.gif;." --add-data "D:/GitHub/Uploader/work_files/updater/update_icon.ico;."  "D:/GitHub/Uploader/work_files/updater/updater.py"

import sys
from PyQt5.QtGui import QMovie, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from update_ui import Ui_MainWindow
from qt_material import apply_stylesheet
import requests
import win32api
import zipfile
import os
import psutil
import subprocess

class Downloader(QObject):
    file_version = pyqtSignal(str)
    github_version = pyqtSignal(str)
    upload_done = pyqtSignal()
    check_version = pyqtSignal(str)
    unzip_file = pyqtSignal()
    del_file = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        try:
            for proc in psutil.process_iter():
                if proc.name() == "AUPAn.exe":
                    proc.kill()
                    break
            if os.path.exists("AUPAn.exe"):
                info = win32api.GetFileVersionInfo("AUPAn.exe", '\\')
                major = info['FileVersionMS'] >> 16
                minor = info['FileVersionMS'] & 0xFFFF
                patch = info['FileVersionLS'] >> 16
                build = info['FileVersionLS'] & 0xFFFF
                version = f"{major}.{minor}.{patch}.{build}"
                self.file_version.emit(version)
            else:
                version = "0.0.0.0"
                self.file_version.emit("Программа не найдена")
        except win32api.error as e:
            version = "0.0.0.0"
            self.file_version.emit(version)
        url = f"https://api.github.com/repos/deathnoragami/uploader_an_dor/releases/latest"
        response = requests.get(url)
        if response.status_code == 200:
            release_info = response.json()
            tag_name = release_info["tag_name"]
            self.github_version.emit(tag_name)
            if version < tag_name:
                link = release_info["assets"][0]["browser_download_url"]
                self.check_version.emit("Начинаю скачивать обновление")
                response = requests.get(link)
                if response.status_code == 200:
                    with open("AUPAn.zip", "wb") as file:
                        file.write(response.content)
                    self.upload_done.emit()
                    self.work_file()
            elif version == tag_name:
                self.check_version.emit("Обновление не нужно")
                
    def work_file(self):
        # patoolib.extract_archive("AUPAn.zip", outdir="./")
        with zipfile.ZipFile('AUPAn.zip', "r") as zip_ref:
            zip_ref.extractall("./")
            
        self.unzip_file.emit()

        try:
            os.remove('AUPAn.zip')
            self.del_file.emit()
        except OSError as e:
            # QMessageBox.warning(None, "Ошибка", "Не смог удалить файлы обновления, программа не имеет админ прав.\nУдалите в папке с программой AUPAn.zip.")
            QMessageBox.warning(None, "Ошибка", f"{e.filename} | {e.strerror}")
                




class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(self.path("update_icon.ico")))
        self.label_right = QLabel(self)
        self.label_right.resize(186, 232)
        self.label_right.move(342, 0)
        dir = self.path("./right_pic.gif")
        self.movie_right = QMovie(dir)
        self.label_right.setMovie(self.movie_right)
        self.movie_right.start()
        self.downloader = Downloader()
        self.downloader.upload_done.connect(self.upload_done)
        self.downloader.github_version.connect(self.github_version)
        self.downloader.file_version.connect(self.file_version)
        self.downloader.check_version.connect(self.check_version)
        self.downloader.unzip_file.connect(self.unzip_file)
        self.downloader.del_file.connect(self.del_file)
        self.thread = QThread()
        self.downloader.moveToThread(self.thread)
        self.thread.started.connect(self.downloader.run)
        self.thread.start()

    def upload_done(self):
        self.ui.label_log.setText(f"{self.ui.label_log.text()} <br>Скачал новую версию")

    def github_version(self, version):
        self.ui.label_log.setText(f"{self.ui.label_log.text()} <br>Версия на гитхабе {version}")
        
    def file_version(self, version):
        self.ui.label_log.setText(f"{self.ui.label_log.text()} <br>Версия файла {version}")
        
    def check_version(self, text):
        self.ui.label_log.setText(f"{self.ui.label_log.text()} <br>{text}")
        if text == "Обновление не нужно":
            subprocess.Popen("AUPAn.exe")
            self.close()
        
    def unzip_file(self):
        self.ui.label_log.setText(f"{self.ui.label_log.text()} <br>Обновление завершено")

    def del_file(self):
        self.ui.label_log.setText(f"{self.ui.label_log.text()} <br>Файлы обновления удалены")
        subprocess.Popen("AUPAn.exe")
        self.close()

    def path(self, path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath('.')
        return os.path.join(base_path, path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue.xml')
    
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())