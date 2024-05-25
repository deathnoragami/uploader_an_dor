from playwright.sync_api import sync_playwright
import log_config
import re


class DoramaUpOther:
    def __init__(self):
        super().__init__()

    def malfurik_checker(self, link, number):
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                context = browser.new_context(storage_state="assets/malfurik_storage.json")
                context.set_default_timeout(120000)
                page = context.new_page()
                page.goto(link)
                all_title = page.query_selector_all(".rwmb-clone.rwmb-group-clone")
                for title in all_title:
                    input_number = title.query_selector("[id^='themeum_video_info_title']").get_attribute("value")
                    if number in input_number:
                        input_video = title.query_selector("[id^='themeum_video_link']").get_attribute("value")
                        context.close()
                        browser.close()
                        return input_video
                context.close()
                browser.close()
                return None
        except Exception as e:
            context.close()
            browser.close()
            log_config.setup_logger().exception(e)
            return None

    def doramatv_uploader(self, link, number, input_video):
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                context = browser.new_context(storage_state="assets/findanime_storage.json")
                context.set_default_timeout(120000)
                page = context.new_page()
                page.goto(link)
                rows = page.query_selector_all('.item-row')
                seria_link = None
                for row in rows:
                    title_element = row.query_selector('.item-title')
                    item_text = title_element.inner_text().strip()
                    if number in item_text:
                        match = re.search(r'\d+', item_text)
                        if match:
                            number_site = int(match.group())
                            if number_site == int(number):
                                link_element = title_element.query_selector('a')
                                seria_link = link_element.get_attribute('href')
                                seria_link = "https://doramatv.live" + seria_link
                                break
                if seria_link:
                    page.goto(seria_link)
                    upload_link = page.query_selector('td[colspan="2"] a')
                    if upload_link:
                        link = upload_link.get_attribute('href')
                        page.goto("https://doramatv.live" + link)
                else:
                    upload_link = page.query_selector('a[data-original-title="Добавить новые серии"]')
                    if upload_link:
                        link = upload_link.get_attribute('href')
                        page.goto("https://doramatv.live" + link)
                        number_input = page.query_selector('.chapter-num')
                        if number_input:
                            number_input.fill(number)
                text_area = f'<iframe allowfullscreen="" src="https://anime.malfurik.online/play.php?video={input_video}" style="border: medium none;" width="100%" height="100%" frameborder="0"></iframe>'
                page.query_selector('#url').fill(text_area)
                page.query_selector('#translationType').select_option("VOICE")
                select_team = page.query_selector('.select-role-null.form-control input')
                if select_team.get_attribute('placeholder') is not None:
                    if select_team:
                        select_team.type("Animaunt")
                        page.wait_for_timeout(1000)
                        page.click('.option.active')
                # page.click('.btn.btn-success.btn-lg')
                page.wait_for_timeout(10000)
                if seria_link is not None:
                    context.close()
                    browser.close()
                    return seria_link
                else:
                    page.goto(link)
                    rows = page.query_selector_all('.item-row')
                    for row in rows:
                        title_element = row.query_selector('.item-title')
                        item_text = title_element.inner_text().strip()
                        if number in item_text:
                            match = re.search(r'\d+', item_text)
                            if match:
                                number_site = int(match.group())
                                if number_site == int(number):
                                    link_element = title_element.query_selector('a')
                                    seria_link = link_element.get_attribute('href')
                                    seria_link = "https://doramatv.live" + seria_link
                                    break
                    if seria_link == None:
                        context.close()
                        browser.close()
                        return None
                    context.close()
                    browser.close()
                    return seria_link
        except Exception as e:
            context.close()
            browser.close()
            log_config.setup_logger().exception(e)
            return None
