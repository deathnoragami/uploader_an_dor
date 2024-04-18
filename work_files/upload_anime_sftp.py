from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from work_files.messagebox_q import CustomMessageBox
import os
import pysftp
import time
from config import Config
from datetime import datetime
import socket
import string
import log_config


class SftpSignals(QObject):
    progress_changed = pyqtSignal(int, float, float, float)

class SFTPManager(QObject):
    def __init__(self):
        super().__init__()
        self.signals = SftpSignals()

    def upload_file(self, dirname, file_path):
        try:
            user_data = Config().get_info_maunt()
            maunt_login = user_data[0]
            maunt_pass = user_data[1]
            
            self.start_time = None
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None

            with pysftp.Connection(os.getenv("ANIMAUNT_IP_SERVER"), username=maunt_login, password=maunt_pass, port=22, cnopts=cnopts) as sftp:
                sock = sftp._transport.sock
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 200 * 1024 * 1024)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 200 * 1024 * 1024)
                sftp.chdir(f'/home/video/mp4/{dirname}')
                sftp.put(file_path, callback=self.progress)
                time_upload = datetime.fromtimestamp(sftp.stat(os.path.basename(file_path)).st_mtime).strftime('%d.%m.%Y %H:%M')
                sftp.close()
                return True, time_upload
        except Exception as e:
            log_config.setup_logger().exception(e)
            QMessageBox.warning(None, "Ошибка", f"Ошибка при загрузке: {e}")
            return False, ""

            
    def search_folder_sftp(self, name_folder):
        try:
            user_data = Config().get_info_maunt()
            maunt_login = user_data[0]
            maunt_pass = user_data[1]
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            
            with pysftp.Connection(os.getenv("ANIMAUNT_IP_SERVER"), username=maunt_login, password=maunt_pass, port=22, cnopts=cnopts) as sftp:
                sftp.chdir('/home/video/mp4')
                name_folder = ''.join(char if char not in string.punctuation else ' ' for char in name_folder).lower().replace("  ", " ")
                found_folder = False
                list_dir = sorted(sftp.listdir_attr(), key=lambda k: k.st_mtime, reverse=True)
                for attr in list_dir:
                    folder_sftp = ''.join(char if char not in string.punctuation else ' ' for char in attr.filename).lower().replace("  ", " ")
                    if name_folder in folder_sftp:
                        dirname = attr.filename
                        found_folder = True
                        break
                if found_folder == False:
                    QMessageBox.warning(None, "Ошибка", "Не найдена папка на сервере")
                    sftp.close()
                    return False
                else:
                    q = CustomMessageBox("Оповещение", f"Найден каталог {dirname}. Верная папка?")
                    if q.show():
                        return dirname
                    else:
                        sftp.close()
                        return False
        except Exception as e:
            sftp.close()
            log_config.setup_logger().exception(e)
                    
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

        



