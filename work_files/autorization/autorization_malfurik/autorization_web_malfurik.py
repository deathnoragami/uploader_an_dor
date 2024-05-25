from playwright.sync_api import sync_playwright
from PyQt5.QtWidgets import QMessageBox

import os
import log_config

class Malfurik_web():
    def __init__(self, checker=False):
        if checker == False:
            try:
                with sync_playwright() as playwright:
                    browser = playwright.chromium.launch(headless=False)
                    if os.path.exists("assets/malfurik_storage.json"):
                        context = browser.new_context(storage_state="assets/malfurik_storage.json")
                        page = context.new_page()
                        link = "https://anime.malfurik.online/"
                    else:
                        context = browser.new_context()
                        page = context.new_page()
                        link = os.getenv('MALFURIK_LINK')
                    page.set_default_timeout(120000)
                    page.goto(link)
                    wpadminbar_element = page.query_selector('#wpadminbar')
                    if wpadminbar_element:
                        QMessageBox.information(None, "Информация", "Вы залогинены.")
                        context.close()
                        browser.close()
                    else:
                        link = os.getenv('MALFURIK_LINK')
                        page.goto(link)
                        try:
                            page.wait_for_selector("#dashboard-widgets-wrap", timeout=20000)
                            context.storage_state(path='assets/malfurik_storage.json')
                            context.close()
                            browser.close()
                        except Exception as e:
                            QMessageBox.warning(None, "Ошибка", "Вы не успели войти, повторите попытку.")
                
            except Exception as e:
                log_config.setup_logger().exception(e)

    def checker(self):
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                context = browser.new_context(storage_state="assets/malfurik_storage.json")
                page = context.new_page()
                page.set_default_timeout(120000)
                link = "https://anime.malfurik.online/"
                page.goto(link)
                wpadminbar_element = page.query_selector('#wpadminbar')
                if wpadminbar_element:
                    context.close()
                    browser.close()
                    return True
                else:
                    context.close()
                    browser.close()
                    return False
        except Exception as e:
            log_config.setup_logger().exception(e)
            context.close()
            browser.close()
            return False