from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from connect_firebase import Connect
import os
import pysftp
import time
from config import Config
from datetime import datetime
import socket
import string


class SftpSignals(QObject):
    progress_changed = pyqtSignal(int, float, float, float)
    finished = pyqtSignal(str, str)

class SFTPManager(QObject):
    def __init__(self):
        super().__init__()
        self.signals = SftpSignals()

    def upload_file(self, dirname, file_path, name_folder):
        db = Connect()
        uid = Config().get_uid_program()
        user_data = db.find_user_uid(uid)
        maunt_login = user_data.get('maunt_login')
        maunt_pass = user_data.get('maunt_pass')
        db.close()
        
        self.start_time = None
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        with pysftp.Connection(os.getenv("ANIMAUNT_IP_SERVER"), username=maunt_login, password=maunt_pass, port=22, cnopts=cnopts) as sftp:
            sock = sftp._transport.sock
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 200 * 1024 * 1024)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 200 * 1024 * 1024)
            sftp.chdir('/home/video/mp4')
            try:
                if dirname and dirname != '':
                    sftp.chdir(dirname)
                    sftp.put(file_path, callback=self.progress)
                    time_upload = datetime.fromtimestamp(sftp.stat(os.path.basename(file_path)).st_mtime).strftime('%d.%m.%Y %H:%M')
                    sftp.close()
                    self.signals.finished.emit(dirname, time_upload)
                else:
                    name_folder = ''.join(char for char in name_folder if char not in string.punctuation)
                    found_folder = False
                    list_dir = sorted(sftp.listdir_attr(), key=lambda k: k.st_mtime, reverse=False)
                    for attr in list_dir:
                        folder_sftp = ''.join(char for char in attr.filename if char not in string.punctuation)
                        if name_folder.lower() in folder_sftp.lower():
                            dirname = attr.filename
                            found_folder = True
                            break
                        
                    if found_folder == False:
                        QMessageBox.warning(None, "Ошибка", "Не найдена папка на сервере")
                        sftp.close()
                        return False
                    else:
                        reply = QMessageBox.question(None, "Оповещение", f"Найден каталог {dirname}. Верная папка?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                        reply.button(QMessageBox.Yes).setText("Да")
                        reply.button(QMessageBox.No).setText("Нет")
                        if reply == QMessageBox.Yes:
                            sftp.chdir(dirname)
                            sftp.put(file_path)
                            time_upload = datetime.fromtimestamp(sftp.stat(os.path.basename(file_path)).st_mtime).strftime('%d.%m.%Y %H:%M')
                            self.signals.finished.emit(dirname, time_upload)
                            return True
                        else:
                            return False
            except Exception as e:
                return False
                    
    def progress(self, transferred, total):
        if self.start_time is None:
            self.start_time = time.time()
        elapsed_time = time.time() - self.start_time
        mb_transferred = transferred / (1024 * 1024)
        if elapsed_time == 0:
            elapsed_time = 0.1
        speed = mb_transferred / elapsed_time
        mb_total = total / (1024 * 1024)
        percent = transferred / total * 100
        self.signals.progress_changed.emit(int(percent), float(mb_transferred), float(mb_total), float(speed))
                
                
        # time_upload = '20.02.2024'
        # for i in range(1, 101):
        #     self.signals.progress_changed.emit(i)
        #     time.sleep(0.1)
        #     self.signals.finished.emit(dirname, time_upload)
        



