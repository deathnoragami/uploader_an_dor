from playwright.sync_api import sync_playwright
from PyQt5.QtWidgets import QMessageBox

import os

class Malfurik_web():
    def __init__(self):
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()
                link = os.getenv('MALFURIK_LINK')
                page.goto(link)
                try:
                    page.wait_for_selector("#dashboard-widgets-wrap", timeout=2000)
                    context.storage_state(path='assets/malfurik_storage.json')
                    context.close()
                    browser.close()
                except Exception as e:
                    QMessageBox.warning(None, "Ошибка", "Вы не успели войти, повторите попытку.")
              
        except Exception as e:
            QMessageBox.warning(None, "Ошибка", e)
