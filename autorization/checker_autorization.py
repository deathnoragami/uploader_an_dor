from autorization.autorization_vk_site.autorization_web_vk import AutorizationWebVK
from autorization.autorization_animaunt.autorization_web_animaunt import Animaunt_web
from autorization.autorization_malfurik.autorization_web_malfurik import Malfurik_web
from PyQt5.QtCore import QThread, pyqtSignal
import os

class CheckerThread(QThread):
    # Сигналы для отправки результата выполнения функции в основной поток
    finished = pyqtSignal(bool, bool, bool)

    def run(self):
        try:
            if os.path.exists("./assets/vk_storage.json"):
                vk_check = AutorizationWebVK(checker=True).check_autorezade(link="https://vk.com/", checker=True)
            else:
                vk_check = False
            
            if os.path.exists("./assets/animaunt_storage.json"):
                ani_check = Animaunt_web(True).checker()
            else:
                ani_check = False

            if os.path.exists("./assets/malfurik_storage.json"):
                malf_check = Malfurik_web(True).checker()
            else:
                malf_check = False
            # vk_check, malf_check, ani_check = True, True, True
            # Отправка результата в основной поток через сигнал
            self.finished.emit(malf_check, ani_check, vk_check)
        except Exception as e:
            os.remove("./assets/vk_storage.json")
            os.remove("./assets/animaunt_storage.json")
            os.remove("./assets/malfurik_storage.json")
            self.finished.emit(False, False, False)
