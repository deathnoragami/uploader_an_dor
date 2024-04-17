import requests
import os
import zipfile
import ctypes
import subprocess
import psutil
import log_config

class FixTimming:
    def __init__(self) -> None:
        pass

    def check_administration(self):
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            return False, "Запустите программу от имени администратора!"
        else:
            return self.check_premier()

    def check_premier(self):
        premier_open = False
        for proc in psutil.process_iter(['pid', 'name']):
            if "Adobe Premiere Pro.exe" in proc.info['name']:
                premier_open = True
        if premier_open == True:
            return False, "Премьер запущен"
        else:
            return self.start_work()
    
    def start_work(self):
        try:
            url = os.getenv('URL_FIX_TIMMING')
            with requests.get(url) as r:
                path = os.path.join(os.getcwd(), 'Add_Keys.reg')
                with open(path, 'wb') as f:
                    f.write(r.content)
            subprocess.run(["regedit", "/s", path], shell=True)
            url = os.getenv('URL_FIX_TIMMING_EX')
            extract_path = r"C:\Program Files (x86)\Common Files\Adobe\CEP\extensions"
            os.makedirs(extract_path, exist_ok=True)
            with requests.get(url) as r:
                path = os.path.join(os.getcwd(), 'pymiere_link.zip')
                with open(path, 'wb') as f:
                    f.write(r.content)
                with zipfile.ZipFile('pymiere_link.zip', "r") as zip_ref:
                    zip_ref.extractall(extract_path)
            os.remove("./Add_Keys.reg")
            os.remove("./pymiere_link.zip")
            return True, "Успех!"
        except Exception as e:
            log_config.setup_logger().exception(e)
            return False, e

            