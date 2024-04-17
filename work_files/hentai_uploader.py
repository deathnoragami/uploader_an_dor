from PyQt5.QtCore import *
import requests
import log_config

class HentaiUploader(QThread):
    add_link = pyqtSignal(str)
    def __init__(self, list_files, api, mail):
        super().__init__()
        self.files = list_files
        self.data = {
            'email': mail,
            'key': api,
        }

    def run(self):
        for file in self.files:
            self.add_link.emit("Загружаю...")
            try:
                r_file = {
                    'file': open(file, 'rb'),
                }
                response = requests.post(
                    'https://ul.mixdrop.ag/api',
                    data=self.data,
                    files=r_file,
                    stream=True,
                )
                url = response.json()['result']['embedurl']
                self.add_link.emit(url)
            except Exception as e:
                log_config.setup_logger().exception(e)
                self.add_link.emit(f"Ошибка загрузки {e}")

            response.close()


