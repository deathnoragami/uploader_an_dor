from autorization.autorization_vk_site.autorization_web_vk import AutorizationWebVK
from autorization.autorization_animaunt.autorization_web_animaunt import Animaunt_web
from autorization.autorization_malfurik.autorization_web_malfurik import Malfurik_web
from PyQt5.QtCore import QThread, pyqtSignal
import os
from playwright.sync_api import sync_playwright


class CheckerThread(QThread):
    # Сигналы для отправки результата выполнения функции в основной поток
    finished = pyqtSignal(bool)

    def run(self):
        vk_check = False
        ani_check = False
        malf_check = False

        with sync_playwright() as pl:
            browser = pl.chromium.launch(headless=True)

            if os.path.exists("./assets/vk_storage.json"):
                try:
                    context = browser.new_context(storage_state="assets/vk_storage.json")
                    page = context.new_page()
                    page.goto("https://vk.com/")
                    if page.url.format() != "https://vk.com/":
                        vk_check = True
                    else:
                        os.remove("./assets/vk_storage.json")
                    context.close()
                except:
                    pass
            # if os.path.exists("./assets/animaunt_storage.json"):
            #     try:
            #         context = browser.new_context(storage_state="assets/animaunt_storage.json")
            #         page = context.new_page()
            #         page.goto(os.getenv('ANIMAUNT_LINK'))
            #         try:
            #             page.wait_for_selector(".sidebar-user-material", timeout=20000)
            #             ani_check = True
            #         except:
            #             os.remove("./assets/animaunt_storage.json")
            #         context.close()
            #     except:
            #         pass
            # if os.path.exists("./assets/malfurik_storage.json"):
            #     try:
            #         context = browser.new_context(storage_state="assets/malfurik_storage.json")
            #         page = context.new_page()
            #         page.goto("https://anime.malfurik.online/")
            #         wpadminbar_element = page.query_selector('#wpadminbar')
            #         if wpadminbar_element:
            #             malf_check = True
            #         else:
            #             os.remove("./assets/malfurik_storage.json")
            #         context.close()
            #     except:
            #         pass
            browser.close()
            malf_check = True
            ani_check = True

        self.finished.emit(vk_check)
