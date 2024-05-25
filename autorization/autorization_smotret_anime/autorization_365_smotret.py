from playwright.sync_api import sync_playwright
import os
import log_config


class _365_Web():
    def __init__(self):
        pass

    def autorization(self):
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=False)
                if os.path.exists("assets/anime365_storage.json"):
                    context = browser.new_context(storage_state="assets/anime365_storage.json")
                else:
                    context = browser.new_context()
                context.set_default_timeout(120000)
                page = context.new_page()
                page.goto("https://anime365.ru/users/login")
                if page.query_selector(".card-image.hide-on-small-and-down"):
                    context.close()
                    browser.close()
                    return True
                else:
                    page.wait_for_selector(".card-image.hide-on-small-and-down")
                    context.storage_state(path='assets/anime365_storage.json')
                    context.close()
                    browser.close()
                    return True
        except Exception as e:
            log_config.setup_logger().exception(e)
            return False
