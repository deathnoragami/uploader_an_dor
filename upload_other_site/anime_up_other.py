from playwright.sync_api import sync_playwright
import re
import os
import log_config


class AnimeUpOther:
    def __init__(self):
        super().__init__()

    def animaunt_checker(self, link, number) -> bool | list:
        try:
            return_data = []
            seria = f'{number} серия'
            with sync_playwright() as pl:
                browser = pl.chromium.launch(headless=False)
                context = browser.new_context(storage_state="./assets/animaunt_storage.json")
                page = context.new_page()
                page.goto(link)
                page.query_selector(".legitRipple.tabPlayerLink").click()
                tabplayer1 = page.wait_for_selector('#tabplayer1')
                divs = tabplayer1.query_selector_all('.col-sm-12.playerNewBlock1')
                for div in divs:
                    input_element = div.query_selector('input')
                    input_value = input_element.get_attribute('value')
                    if input_value == seria:
                        code_element = input_element.query_selector('xpath=./following-sibling::input')
                        code_value = code_element.get_attribute('value')
                        return_data.append(code_value)
                        return_data.append(code_value.split('/')[-1])
                if return_data:
                    page.close()
                    browser.close()
                    return True, return_data
                else:
                    page.close()
                    browser.close()
                    return False, ["Не нашел нужной серии"]
        except Exception as e:
            log_config.setup_logger().exception(e)
            return False, list(e)

    def findanime(self, link_title, number, code) -> bool | str:
        with sync_playwright() as pl:
            browser = pl.chromium.launch(headless=False)
            context = browser.new_context(storage_state="./assets/findanime_storage.json")
            page = context.new_page()
            page.goto(link_title)
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
                            seria_link = "https://findanime.net" + seria_link
                            break
            if seria_link:
                page.goto(seria_link)
                upload_link = page.query_selector('td[colspan="2"] a')
                if upload_link:
                    link = upload_link.get_attribute('href')
                    page.goto("https://findanime.net" + link)
            else:
                upload_link = page.query_selector('a[data-original-title="Добавить новые серии"]')
                if upload_link:
                    link = upload_link.get_attribute('href')
                    page.goto("https://findanime.net" + link)
                    number_input = page.query_selector('.chapter-num')
                    if number_input:
                        number_input.fill(number)
            text_area = f'<iframe allowfullscreen src="//animaunt.org/{code}"> </iframe>'
            page.query_selector('#url').fill(text_area)
            page.query_selector('#translationType').select_option("VOICE_MULTI")
            select_team = page.query_selector('.select-role-null.form-control input')
            if select_team.get_attribute('placeholder') is not None:
                if select_team:
                    select_team.type("Animaunt")
                    page.wait_for_timeout(1000)
                    page.click('.option.active')
            page.click('.btn.btn-success.btn-lg')
            page.wait_for_timeout(1000)
            if seria_link is not None:
                return True, seria_link
            else:
                page.goto(link_title)
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
                                seria_link = "https://findanime.net" + seria_link
                                break
                if seria_link == None:
                    return False, ''
                return True, seria_link

    def anime365(self, title_link, number, path) -> bool | str:
        with sync_playwright() as pl:
            browser = pl.chromium.launch(headless=False)
            context = browser.new_context(storage_state="./assets/anime365_storage.json")
            page = context.new_page()
            page.goto(title_link)
            episode_elements = page.query_selector_all('.card-content.m-episode-list .col.s12.m6.l4.x3')
            episode_link = None
            for episode in episode_elements:
                episode_text = episode.inner_text().strip()
                episode_text = episode_text.replace("play_circle_filled", "").strip()
                if number in episode_text:
                    match = re.search(r'\d+', episode_text)
                    if match:
                        number_site = int(match.group())
                        if number_site == int(number):
                            episode_link_element = episode.query_selector('a')
                            episode_link = episode_link_element.get_attribute('href')
                            break
            if episode_link:
                page.goto("https://anime365.ru" + episode_link)
                page.query_selector('.m-translation-back-links a[href*="/translations/create"]').click()
                page.wait_for_selector('.input-field.col.s6.l3 .select-dropdown')
                input_element = page.query_selector_all('.input-field.col.s6.l3 .select-dropdown')
            else:
                page.query_selector('.m-translation-back-links a[href*="/translations/create"]').click()
                page.wait_for_selector('#TranslationAdminForm_episodeNumberNew')
                page.query_selector('#TranslationAdminForm_episodeNumberNew').fill(number)
                page.wait_for_selector('.input-field.col.s6.l3 .select-dropdown')
                input_element = page.query_selector_all('.input-field.col.s6.l3 .select-dropdown')
                if input_element[0]:
                    input_element[0].click()
                    page.wait_for_timeout(1000)
                    all_options = page.query_selector_all('ul.dropdown-content.select-dropdown li')
                    for option in all_options:
                        option_text = option.inner_text()
                        if option_text == 'TV':
                            option.click()
                            break
            if input_element[2]:
                input_element[2].click()
                page.wait_for_timeout(1000)
                all_options = page.query_selector_all('ul.dropdown-content.select-dropdown li')
                for option in all_options:
                    option_text = option.inner_text()
                    if option_text == 'Озвучка':
                        option.click()
                        break

            page.query_selector('#TranslationAdminForm_authorsNew').fill('Animaunt')

            page.query_selector('.qq-upload-button-selector input[type="file"]').set_input_files(
                path)
            page.wait_for_selector('.qq-upload-success', timeout=300000)
            page.query_selector('button[name="yt0"]').click()
            page.wait_for_timeout(5000)
            page.wait_for_selector('.card-content')
            episode_link = page.query_selector('.card-content a').get_attribute("href")
            return True, episode_link

