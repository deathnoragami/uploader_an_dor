from playwright.sync_api import sync_playwright
from PyQt5.QtWidgets import QMessageBox
import os

class AutorizationWebVK():
    def __init__(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            vk_link = "https://vk.com/"
            page.goto(vk_link)
            try:
                page.wait_for_selector("#l_nwsf", timeout=120000)
                storage = context.storage_state(path="assets/vk_storage.json")
                context.close()
                browser.close()
            except Exception as e:
                QMessageBox.warning(None, "Не зашли в аккаунт!", "Вы не авторизовались в аккаунте.")
                context.close()
                browser.close()

        
        if os.path.isfile('assets/vk_storage.json'):
            self.check_autorezade(vk_link)
    
    def check_autorezade(self, link):
        with sync_playwright() as pl:
            browser1 = pl.chromium.launch(headless=True)
            context1 = browser1.new_context(storage_state="assets/vk_storage.json")
            page1 = context1.new_page()
            page1.goto(link)
            if page1.url.format() == link:
                QMessageBox.warning(None, "Ошибка", "Авторизация не сохранилась, повторите попытку")
                context1.close()
                browser1.close()
            else:
                QMessageBox.information(None, "Информация", "Авторизация успешно сохранена")

    
