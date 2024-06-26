from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal
import pysftp
import time
import socket
import string
from datetime import datetime
from config import Config
import os
import log_config


class SftpSignals(QObject):
    progress_changed = pyqtSignal(int, float, float, float)

class UploadDoramaSFTP(QObject):
    def __init__(self, main_ui = None):
        super().__init__()
        self.signals = SftpSignals()
        self.start_time = None
        self.main_ui = main_ui
        
    def search_folder_sftp(self, file_path):
        user_data = Config().get_info_malf()
        malf_login = user_data[0]
        malf_pass = user_data[1]
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(host=os.getenv("MALFURIK_IP_SERVER"), username=malf_login, password=malf_pass, port=22, cnopts=cnopts) as sftp:
            sftp.chdir('/home/video/mp4')
            name_folder = os.path.basename(os.path.dirname(file_path))
            name_folder = ''.join(char if char not in string.punctuation else ' ' for char in name_folder).lower().replace("  ", " ")
            list_dir = sorted(sftp.listdir_attr(), key=lambda k: k.st_mtime, reverse=True)
            found_folder = None
            for attr in list_dir:
                folder_sftp = ''.join(char if char not in string.punctuation else ' ' for char in attr.filename).lower().replace("  ", " ")
                if name_folder in folder_sftp:
                    return attr.filename
                    # q = QMessageBox.question(None, "[SFTP] Что-то нашел", f"[SFTP] Папка на сервере называется\n {attr.filename} ?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
                    # if q == QMessageBox.Yes:
                    #     found_folder = attr.filename
                    #     sftp.close()
                    #     return found_folder
                    # elif q == QMessageBox.No:
                    #     continue
                    # else:
                    #     sftp.close()
                    #     return None
            if not found_folder:
                QMessageBox.warning(None, "[SFTP] Поиск", "[SFTP] Не смог найти папку. Убедитесь в названии у себя на компьютере или на сервере")
                sftp.close()
                return None
            
    def upload_sftp(self, file_path, folder_sftp):
        try:
            user_data = Config().get_info_malf()
            malf_login = user_data[0]
            malf_pass = user_data[1]
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            with pysftp.Connection(host=os.getenv("MALFURIK_IP_SERVER"), username=malf_login, password=malf_pass, port=22, cnopts=cnopts) as sftp:
                sock = sftp._transport.sock
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 200 * 1024 * 1024)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 200 * 1024 * 1024)
                sftp.chdir(f'/home/video/mp4/{folder_sftp}')
                sftp.put(file_path, callback=self.progress)
                time_upload = datetime.fromtimestamp(sftp.stat(os.path.basename(file_path)).st_mtime).strftime('%d.%m.%Y %H:%M')
                sftp.close()
                return True, time_upload
        except Exception as e:
            log_config.setup_logger().exception(e)
            QMessageBox.warning(None, "Ошибка", f"Произошла ошибка при загрузки файла\n{e}")
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