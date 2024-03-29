from playwright.sync_api import sync_playwright
from PyQt5.QtWidgets import QMessageBox

import os

class Animaunt_web():
    def __init__(self):
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=False)
                if os.path.exists("assets/animaunt_storage.json"):
                    context = browser.new_context(storage_state="assets/animaunt_storage.json")
                else:
                    context = browser.new_context()
                page = context.new_page()
                link = os.getenv('ANIMAUNT_LINK')
                page.goto(link)
                try:
                    page.wait_for_selector(".sidebar-user-material", timeout=120000)
                    context.storage_state(path='assets/animaunt_storage.json')
                    context.close()
                    browser.close()
                except Exception as e:
                    QMessageBox.warning(None, "Ошибка", "Вы не успели войти, повторите попытку.")
                
        except Exception as e:
            QMessageBox.warning(None, "Ошибка", e)
