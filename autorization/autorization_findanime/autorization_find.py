from playwright.sync_api import sync_playwright
import os
import log_config


class AnimeFind_Web():
    def __init__(self):
        pass

    def autorization(self):
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=False)
                if os.path.exists("assets/findanime_storage.json"):
                    context = browser.new_context(storage_state="assets/findanime_storage.json")
                else:
                    context = browser.new_context()
                context.set_default_timeout(120000)
                page = context.new_page()
                page.goto(
                    "https://grouple.co/internal/auth/login?targetUri=%2Flogin%2FcontinueSso%3FtargetUri%3Dhttps%253A%252F%252Ffindanime.net%252F%26siteId%3D4&siteId=4")
                if page.query_selector(".header-item.dropdown.user-profile-settings-link"):
                    context.close()
                    browser.close()
                    return True
                else:
                    page.wait_for_selector(".header-item.dropdown.user-profile-settings-link")
                    page.goto("https://doramatv.live/")
                    page.query_selector(".strong.nav-link.login-link").click()
                    context.storage_state(path='assets/findanime_storage.json')
                    context.close()
                    browser.close()
                    return True
        except Exception as e:
            log_config.setup_logger().exception(e)
            return False
