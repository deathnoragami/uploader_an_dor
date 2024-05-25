from PyQt5.QtCore import QThread, pyqtSignal
import os
import subprocess
import pysftp


class VersionChecker(QThread):
    check_version = pyqtSignal(bool)

    def __init__(self, version):
        super(VersionChecker, self).__init__()
        self.version = version

    def run(self):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        # Создаем экземпляр главного окна только если условие не выполнено
        with pysftp.Connection(host=os.getenv("FTP_HOST"), username=os.getenv("FTP_USER"),
                               password=os.getenv("FTP_PASS"), port=22,
                               cnopts=cnopts) as ftp:
            ftp.chdir('AUPAn')
            version_ftp = ftp.listdir()[0]
            if self.version < version_ftp:
                if os.path.exists("update.exe"):
                    subprocess.Popen(["update.exe"])


                

