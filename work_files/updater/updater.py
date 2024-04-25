# pyinstaller --noconfirm --onefile --windowed --icon "C:/Python/uploader_an_dor/work_files/updater/update_icon.ico" --name "update" --add-data "C:/Python/uploader_an_dor/work_files/updater/right_pic.gif;." --add-data "C:/Python/uploader_an_dor/work_files/updater/update_icon.ico;."  "C:/Python/uploader_an_dor/work_files/updater/updater.py"
# pyinstaller --noconfirm --onefile --windowed --icon "D:/GitHub/Uploader/work_files/updater/update_icon.ico" --name "update" --add-data "D:/GitHub/Uploader/work_files/updater/update_icon.ico;."  "D:/GitHub/Uploader/work_files/updater/updater.py"
import shutil
import subprocess
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from update_ui import Ui_MainWindow
import win32api
import zipfile
import os
import psutil
import pysftp
import const
import socket


class Downloader(QThread):
    progress = pyqtSignal(int)
    complete_download = pyqtSignal()
    install_file = pyqtSignal()
    complete = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(host=const.HOST, username=const.USER, password=const.PASSWORD, port=22,
                               cnopts=cnopts) as ftp:
            sock = ftp._transport.sock
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 200 * 1024 * 1024)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 200 * 1024 * 1024)
            ftp.chdir('AUPAn')
            ftp.get("AUPAn.zip", "AUPAn.zip", self.call)
            ftp.close()
            self.complete_download.emit()
        self.install_file.emit()
        delete = self.del_file()
        if delete:
            self.work_file()

    def call(self, transferred, total):
        percent = transferred / total * 100
        self.progress.emit(int(percent))

    def del_file(self):
        try:
            for proc in psutil.process_iter():
                if proc.name() == "AUPAn.exe":
                    proc.kill()
                    break
            try:
                shutil.rmtree("_internal")
            except:
                pass
            try:
                os.remove("AUPAn.exe")
            except:
                pass
            return True
        except Exception as e:
            return False

    def work_file(self):
        try:
            # patoolib.extract_archive("AUPAn.zip", outdir="./")
            with zipfile.ZipFile('AUPAn.zip', "r") as zip_ref:
                zip_ref.extractall("./")
            try:
                os.remove('AUPAn.zip')
            except OSError as e:
                # QMessageBox.warning(None, "Ошибка", "Не смог удалить файлы обновления, программа не имеет админ прав.\nУдалите в папке с программой AUPAn.zip.")
                QMessageBox.warning(None, "Ошибка", f"{e.filename} | {e.strerror}")
            self.complete.emit()
        except Exception as e:
            print(e)


class MainWindow(QMainWindow):
    def __init__(self, version=None, current_ver=None):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(self.path("update_icon.ico")))
        self.ui.update_version.setText(version)
        self.ui.current_version.setText(current_ver)
        self.ui.pushButton.clicked.connect(self.update)
        self.ui.pushButton_2.clicked.connect(self.close)

    def update(self):
        self.ui.label_9.setText("Загружаю...")
        self.worker = Downloader()
        self.worker.progress.connect(self.progress)
        self.worker.complete_download.connect(self.complete_download)
        self.worker.install_file.connect(self.install_file)
        self.worker.complete.connect(self.complete)
        self.worker.start()
        self.ui.pushButton.setEnabled(False)

    def complete(self):
        self.ui.label_9.setText("Обновлено")
        self.ui.pushButton.setEnabled(True)
        self.ui.pushButton.setText("Открыть программу")
        self.ui.pushButton.clicked.disconnect()
        self.ui.pushButton.clicked.connect(self.open_programm)

    def open_programm(self):
        subprocess.Popen("AUPAn.exe")
        self.close()

    def install_file(self):
        self.ui.label_9.setText("Устанавливаю...")

    def progress(self, cur):
        self.ui.progress_bar.setValue(cur)

    def complete_download(self):
        self.ui.label_9.setText("Файлы загружены")

    def search_version_file(self):
        try:
            if os.path.exists("AUPAn.exe"):
                info = win32api.GetFileVersionInfo("AUPAn.exe", '\\')
                major = info['FileVersionMS'] >> 16
                minor = info['FileVersionMS'] & 0xFFFF
                patch = info['FileVersionLS'] >> 16
                build = info['FileVersionLS'] & 0xFFFF
                version = f"{major}.{minor}.{patch}.{build}"
                return version
            else:
                version = "Программа не найдена"
                return version
        except win32api.error as e:
            version = "0.0.0.0"
            return version

    def path(self, path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath('.')
        return os.path.join(base_path, path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    # Создаем экземпляр главного окна только если условие не выполнено
    with pysftp.Connection(host=const.HOST, username=const.USER, password=const.PASSWORD, port=22,
                           cnopts=cnopts) as ftp:
        ftp.chdir('AUPAn')
        version = ftp.listdir()[0]
        current_ver = MainWindow().search_version_file()
        if version != current_ver:
            main_window = MainWindow(version, current_ver)
            main_window.show()
            sys.exit(app.exec_())
        else:
            app.quit()
