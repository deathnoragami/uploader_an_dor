from PyQt5.QtCore import QThread, pyqtSignal
import requests

class VersionChecker(QThread):
    check_version = pyqtSignal(bool)

    def __init__(self, version):
        super(VersionChecker, self).__init__()
        self.version = version

    def run(self):
        url = f"https://api.github.com/repos/deathnoragami/uploader_an_dor/releases/latest"
        response = requests.get(url)
        if response.status_code == 200:
            release_info = response.json()
            tag_name = release_info["tag_name"]
            if self.version < tag_name:
                self.check_version.emit(True)
            elif self.version == tag_name:
                self.check_version.emit(False)