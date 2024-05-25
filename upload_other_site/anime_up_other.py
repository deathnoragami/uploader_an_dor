from playwright.sync_api import sync_playwright
import re
import sys
import log_config
import logging
from PyQt5.QtCore import pyqtSignal, QObject
import os
import requests
from bs4 import BeautifulSoup
import fake_useragent


class AnimeUpOther(QObject):
    find_anime = pyqtSignal(str, str)
    _365_anime = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()



    def upload_all(self, animaunt_link, findanime_link, _365_link, number, path):
        self.logger.info("Выполнение метода")
        seria = f'{number} серия'
        find_code = False
        try:
            with sync_playwright() as pl:
                browser = pl.chromium.launch(headless=False)
                context = browser.new_context(storage_state="./assets/animaunt_storage.json")
                page = context.new_page()
                page.goto(animaunt_link)
                page.query_selector(".legitRipple.tabPlayerLink").click()
                tabplayer1 = page.wait_for_selector('#tabplayer1')
                divs = tabplayer1.query_selector_all('.col-sm-12.playerNewBlock1')
                for div in divs:
                    input_element = div.query_selector('input')
                    input_value = input_element.get_attribute('value')
                    if input_value == seria:
                        code_element = input_element.query_selector('xpath=./following-sibling::input')
                        code_value = code_element.get_attribute('value')
                        code_player = code_value
                        file_name = code_value.split('/')[-1]
                        find_code = True
                if find_code:
                    pass
                else:
                    context.close()
                    browser.close()
                    self.find_anime.emit("Не открыл")
                    return
                files = os.listdir(path)
                if file_name in files:
                    file_path = os.path.join(path, file_name)
                context3 = browser.new_context(storage_state="./assets/anime365_storage.json")
                page3 = context3.new_page()
                page3.goto(_365_link)
                episode_elements = page3.query_selector_all('.card-content.m-episode-list .col.s12.m6.l4.x3')
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
                    page3.goto("https://anime365.ru" + episode_link)
                    page3.query_selector('.m-translation-back-links a[href*="/translations/create"]').click()
                    page3.wait_for_selector('.input-field.col.s6.l3 .select-dropdown')
                    input_element = page.query_selector_all('.input-field.col.s6.l3 .select-dropdown')
                else:
                    page3.query_selector('.m-translation-back-links a[href*="/translations/create"]').click()
                    page3.wait_for_selector('#TranslationAdminForm_episodeNumberNew')
                    page3.query_selector('#TranslationAdminForm_episodeNumberNew').fill(number)
                    page3.wait_for_selector('.input-field.col.s6.l3 .select-dropdown')
                    input_element = page3.query_selector_all('.input-field.col.s6.l3 .select-dropdown')
                    if input_element[0]:
                        input_element[0].click()
                        page3.wait_for_timeout(1000)
                        all_options = page3.query_selector_all('ul.dropdown-content.select-dropdown li')
                        for option in all_options:
                            option_text = option.inner_text()
                            if option_text == 'TV':
                                option.click()
                                break
                if input_element[2]:
                    input_element[2].click()
                    page3.wait_for_timeout(1000)
                    all_options = page3.query_selector_all('ul.dropdown-content.select-dropdown li')
                    for option in all_options:
                        option_text = option.inner_text()
                        if option_text == 'Озвучка':
                            option.click()
                            break

                page3.query_selector('#TranslationAdminForm_authorsNew').fill('Animaunt')

                page3.query_selector('.qq-upload-button-selector input[type="file"]').set_input_files(
                    file_path)
                page3.wait_for_selector('.qq-upload-success', timeout=300000)
                page3.query_selector('button[name="yt0"]').click()
                page3.wait_for_timeout(5000)
                page3.wait_for_selector('.card-content')
                episode_link = page3.query_selector('.card-content a').get_attribute("href")
                episode_link = "https://anime365.ru" + episode_link
                print(episode_link)
                self._365_anime.emit("365", episode_link)
                context.close()
                browser.close


        except Exception as e:
            self.logger.exception("Ошибка в методе animaunt_checker")
            log_config.setup_logger().exception(e)


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
                    context.close()
                    browser.close()
                    return True, return_data
                else:
                    context.close()
                    browser.close()
                    return False, ["Не нашел нужной серии"]
        except Exception as e:
            log_config.setup_logger().exception(e)
            return False, list(e)

    def findanime(self, link_title, code, number, dorama: bool = False) -> bool | str:
        try:
            if dorama:
                text_area = f'<iframe allowfullscreen src="//anime.malfurik.online/play.php?video={code}"></iframe>'
            else:
                text_area = f'<iframe allowfullscreen src="//animaunt.org/{code}"> </iframe>'
            session = requests.Session()
            if dorama:
                url = "https://grouple.co/login/authenticate?ttt=1715503210854&siteId=5"
            else:
                url = "https://grouple.co/login/authenticate?ttt=1714144489992&siteId=4"
            user = fake_useragent.UserAgent().random
            header = {
                'user-agent' : user
            }
            if dorama:
                data = {
                    "targetUri":r"/login/continueSso?targetUri=https%3A%2F%2Fdoramatv.live%2F&siteId=5",
                    "username": os.getenv("LOGIN_FIND"), 
                    "password": os.getenv("PASS_FIND"), 
                }
            else:
                data = {
                    "targetUri":r"/login/continueSso?targetUri=https%3A%2F%2Ffindanime.net%2F&siteId=4",
                    "username": os.getenv("LOGIN_FIND"), 
                    "password": os.getenv("PASS_FIND"), 
                }
            session.post(url, headers=header, data=data) # Авторизация
            html_text = session.get(link_title, headers=header).text
            soup = BeautifulSoup(html_text, 'html.parser')
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                if href.startswith("/internal/upload/index/"):
                    id_anime  = href.replace("/internal/upload/index/", "") # Айди аните
                    break
            if dorama:
                data_upload = {
                    "seriesType": "SERIES", # Что именно
                    "chapter": number, # Номер серии
                    "url":text_area , # url
                    "translationType": "VOICE", # какая озвучка
                    "personAndType": "39535:4" # команда
                }
            else:
                data_upload = {
                    "seriesType": "SERIES", # Что именно
                    "chapter": number, # Номер серии
                    "url":text_area , # url
                    "translationType": "VOICE_MULTI", # какая озвучка
                    "personAndType": "7035:4" # команда
                }
            if dorama:
                save_url = f'https://doramatv.live/internal/upload/video/save/{id_anime}'
            else:
                save_url = f'https://findanime.net/internal/upload/video/save/{id_anime}'
            upl = session.post(save_url, headers=header, data=data_upload)
            soup_post = BeautifulSoup(upl.text, 'html.parser')
            if soup_post.find(text='Ссылка добавлена') or soup_post.find(text='Такая ссылка уже добавлена в это произведение'):
                html_text = session.get(link_title, headers=header).text
                soup = BeautifulSoup(html_text, 'html.parser')
                rows = soup.select('.item-row')
                for row in rows:
                    title_element = row.select_one('.item-title')
                    item_text = title_element.get_text().strip()
                    if number in item_text:
                        match = re.search(r'\d+', item_text)
                        if match:
                            number_site = int(match.group())
                            if number_site == int(number):
                                link_element = title_element.select_one('a')
                                seria_link = link_element['href']
                                if dorama:
                                    seria_link = "https://doramatv.live" + seria_link
                                else:
                                    seria_link = "https://findanime.net" + seria_link
                                return True, seria_link
            else:
                script_tag = soup_post.find('script', text=re.compile(r'showNoty')).string
                pattern = r'"text":"(.*?)"'
                matches = re.findall(pattern, script_tag)[0]
                return False, "Не смог добавить серию " + matches
            return False, "Не нашел нужной серии"
        except Exception as e:  
            log_config.setup_logger().exception(e)
            False, e
        




        # with sync_playwright() as pl:
        #     browser = pl.chromium.launch(headless=False)
        #     context = browser.new_context(storage_state="./assets/findanime_storage.json")
        #     page = context.new_page()
        #     page.goto(link_title)
        #     rows = page.query_selector_all('.item-row')
        #     seria_link = None
        #     for row in rows:
        #         title_element = row.query_selector('.item-title')
        #         item_text = title_element.inner_text().strip()
        #         if number in item_text:
        #             match = re.search(r'\d+', item_text)
        #             if match:
        #                 number_site = int(match.group())
        #                 if number_site == int(number):
        #                     link_element = title_element.query_selector('a')
        #                     seria_link = link_element.get_attribute('href')
        #                     seria_link = "https://findanime.net" + seria_link
        #                     break
        #     if seria_link:
        #         page.goto(seria_link)
        #         upload_link = page.query_selector('td[colspan="2"] a')
        #         if upload_link:
        #             link = upload_link.get_attribute('href')
        #             page.goto("https://findanime.net" + link)
        #     else:
        #         upload_link = page.query_selector('a[data-original-title="Добавить новые серии"]')
        #         if upload_link:
        #             link = upload_link.get_attribute('href')
        #             page.goto("https://findanime.net" + link)
        #             number_input = page.query_selector('.chapter-num')
        #             if number_input:
        #                 number_input.fill(number)
        #     text_area = f'<iframe allowfullscreen src="//animaunt.org/{code}"> </iframe>'
        #     page.query_selector('#url').fill(text_area)
        #     page.query_selector('#translationType').select_option("VOICE_MULTI")
        #     select_team = page.query_selector('.select-role-null.form-control input')
        #     if select_team.get_attribute('placeholder') is not None:
        #         if select_team:
        #             select_team.type("Animaunt")
        #             page.wait_for_timeout(1000)
        #             page.click('.option.active')
        #     page.click('.btn.btn-success.btn-lg')
        #     page.wait_for_timeout(1000)
        #     if seria_link is not None:
        #         return True, seria_link
        #     else:
        #         page.goto(link_title)
        #         rows = page.query_selector_all('.item-row')
        #         for row in rows:
        #             title_element = row.query_selector('.item-title')
        #             item_text = title_element.inner_text().strip()
        #             if number in item_text:
        #                 match = re.search(r'\d+', item_text)
        #                 if match:
        #                     number_site = int(match.group())
        #                     if number_site == int(number):
        #                         link_element = title_element.query_selector('a')
        #                         seria_link = link_element.get_attribute('href')
        #                         seria_link = "https://findanime.net" + seria_link
        #                         break
        #         if seria_link == None:
        #             return False, ''
        #         return True, seria_link

    def anime365(self, title_link, number, path, browser) -> bool | str:
        try:
            context = browser.new_context(storage_state="./assets/anime365_storage.json")
            page = context.new_page()
            page.set_default_timeout(120000)
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
            episode_link = "https://anime365.ru" + episode_link
            context.close()
            return True, episode_link
        except Exception as e:
            log_config.setup_logger().exception(e)
            context.close()
            return False, e

if __name__ == "__main__":
    link = "https://findanime.net/zabvenie_betteri__tv_"
    code = "play.php?video=https://video.animaunt.tv/Забвение бэттери | Boukyaku Battery (TV)/03x.mp4"
    number = "3"
    AnimeUpOther().findanime(link, code, number)
