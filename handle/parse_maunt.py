import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import fake_useragent
import log_config
from config import Config


class ParseMaunt:
    def __init__(self):
        super().__init__()
        self.data = {}
        self.session = requests.Session()
        user = fake_useragent.UserAgent().random
        self.headers = {
            'user-agent' : user
        }

    def update_seria_maunt(self, link:str, 
                           number_seria:str, 
                           data_calendar:str = None, 
                           name_file:str = None,
                           dorama:bool = False,
                           timer:bool = False):
        if self.autorization_maunt(link):
            if self.get_change_data(number_seria, data_calendar, name_file, dorama, timer):
                if self.get_dont_change_data():
                    if self.data_relise != []:
                        formated = []
                        for key, value in self.data.items():
                            if isinstance(value, list):
                                formated.extend((key, val) for val in value)
                            else:
                                formated.append((key, value))
                        self.data = formated + self.data_relise 

                    update_res = self.session.post(
                        link,
                        headers=self.headers,
                        data=self.data,
                        )
                    if update_res.status_code == 200:
                        return True
                    else: 
                        return None
                else: 
                    return None
            else: 
                return None
        else: 
            return None
            

    def autorization_maunt(self, link):
        a_data = Config().get_a_info_site()
        data = {
            'subaction': 'dologin',
            'username': a_data[0],
            'password': a_data[1],
            'selected_language': 'Russian',
        }
        auth = self.session.post(r'https://animaunt.org/私は独身です.php?mod=main', headers=self.headers, data=data)
        if auth.status_code == 200:
            CSRFResponse = self.session.get("https://animaunt.org/私は独身です.php?mod=main")
            soup = BeautifulSoup(CSRFResponse.text, "html.parser")
            script_tag = soup.find_all("script", type="text/javascript")
            pattern = r'var dle_login_hash = \'(.*?)\';'
            self.dle_login_hash = re.search(pattern, str(script_tag[1])).group(1)
            self.data['user_hash'] = self.dle_login_hash
            adminka = self.session.get(link, headers=self.headers)
            if adminka.status_code == 200:
                self.soup = BeautifulSoup(adminka.content, "html.parser")
                return True
            return None
        else:
            return None

    def get_change_data(self, number_seria, data_calendar=None, name_file=None, dorama=False, timer=False):
        try:
            ####### ДАТА СЛЕД СЕРИИ ############
            timer_next_seria = self.soup.find('input', id='xf_date_timer')['value']
            original_date = datetime.strptime(timer_next_seria, "%Y-%m-%dT%H:%M")
            reform_original_date = original_date.strftime("%Y-%m-%dT%H:%M")
            if dorama == True:
                if timer == True:
                    new_data = original_date + timedelta(weeks=1)
                    reform_new_data = new_data.strftime("%Y-%m-%dT%H:%M")
                    self.data['xfield[date_timer]'] = reform_new_data
                else:
                    data_now = datetime.fromisoformat(datetime.now().isoformat())
                    time_difference = original_date - data_now
                    if time_difference.days > 2:
                        new_data = original_date + timedelta(weeks=2)
                        reform_new_data = new_data.strftime("%Y-%m-%dT%H:%M")
                        self.data['xfield[date_timer]'] = reform_new_data
                    else:
                        self.data['xfield[date_timer]'] = reform_original_date
            else:
                new_date = original_date + timedelta(weeks=1)
                new_date_string = new_date.strftime("%Y-%m-%dT%H:%M")
                self.data['xfield[date_timer]'] = new_date_string

            ####################################

            ###### НОМЕР СЕРИИ ############
            current_seria = self.soup.find('input', id='xf_number_seria')
            self.data[current_seria['name']] = number_seria
            # tuple_current_seria = (current_seria['name'], number_seria)
            # self.data.append(tuple_current_seria)
            ####################################

            ###### НОМЕР СЛЕД СЕРИИ ############
            next_seria = self.soup.find('input', id='xf_date_timer_seria')
            self.data[next_seria['name']] = str(int(number_seria) + 1)
            # tuple_next_seria = (next_seria['name'], str(int(number_seria) + 1))
            # self.data.append(tuple_next_seria)
            ####################################

            ###### ПОЛНЫЙ КАЛЕНДАРЬ ############
            script_tags = self.soup.find_all('script')
            for script_tag in script_tags:
                if 'window.releases' in str(script_tag):
                    text = str(script_tag)
                    pattern = re.compile(r'window\.releases\s*=\s*JSON\.parse\((.*?)\);')
                    match = pattern.search(text)
                    if match:
                        data_string = match.group(1)
                        pattern = re.compile(r'{"title":"(.*?)","date1":"(.*?)","date2":"(.*?)"')
                        matches = pattern.findall(data_string)
                        self.data_relise = []
                        if matches != [('', '', '')]:
                            for match in matches:
                                self.data_relise.extend([
                                    ('release[title][]', match[0]),
                                    ('release[date1][]', match[1]),
                                    ('release[date2][]', match[2])
                                ])
                            break
            if not dorama:
                # НЫНЯШНЯЯ СЕРИЯ
                self.data_relise.extend([
                                    ('release[title][]', f"Эпизод {number_seria}"),
                                    ('release[date1][]', data_calendar),
                                    ('release[date2][]', data_calendar)
                                ])

            ######################################

            
            ##### ТАЙТЛ ВИДЕО И САМИ ВИДЕО ##########
            data_video = []
            title_player = self.soup.find('input', {'name': lambda x: x and 'fplayers[1][title]' in x})
            self.data[title_player['name']] = title_player['value']
            # data_video.append((title_player['name'], title_player['value']))
            inputs = self.soup.find_all('input', {'name': lambda x: x and 'fplayers[1][series]' in x})
            for input_tag in inputs:
                name = input_tag['name']
                value = input_tag['value']
                self.data[name] = value
                data_video.append((name, value))
            if not dorama:
                title_name, title_video, code_name, code_value = self.new_video(data_video, number_seria, name_file)
                self.data[title_name] = title_video
                self.data[code_name] = code_value
            #     data_video.append(new_name)
            #     data_video.append(new_code)
            # self.data.append(data_video)
            ####################################################

            ##### ДАТА И ВРЕМЯ НАСТОЯЩЕЕ ########
            current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.data['newdate'] = current_datetime
            # newdate_tuple = ('newdate', current_datetime)
            # self.data.append(newdate_tuple)
            ##########################
            return True
        except Exception as e:
            log_config.setup_logger().exception(e)
            return None

    def new_video(self, data_video, number_seria, name_file):
        last_name = data_video[-2]
        last_code = data_video[-1]
        pattern_name = r'fplayers\[\d+\]\[series\]\[(\d+)\]\[name\]'
        pattern_fplayers = r'^(fplayers\[\d+\]\[series\])'
        match_fplayers = re.search(pattern_fplayers, last_name[0]).group(1)        
        match_name = re.search(pattern_name, last_name[0]).group(1)
        new_number = int(match_name) + 1
        name = f"{match_fplayers}[{new_number}][name]"
        name_value = f'{number_seria} серия'
        code = f"{match_fplayers}[{new_number}][code]"
        if name_file == None:
            string = last_code[1].split("/")
            match = re.search(r'(\d+)(x?)(?=\.\w+$)', string[-1])
            file_number = int(match.group(1))
            x_symbol = match.group(2)
            new_file_number = file_number + 1
            new_file_number = f"{new_file_number:02d}{x_symbol}"
            name_file = re.sub(r'(\d+)(x?)(?=\.\w+$)', new_file_number, string[-1])
        index = last_code[1].rfind("/")
        if index != -1:
            match_code = last_code[1][:index]
        code_value = f'{match_code}/{name_file}'
        return name, name_value, code, code_value
        
    def get_dont_change_data(self):
            default = {
                'date_calendar': '0',
                'name[1]': '1 серия',
                'approve': '1',
                'allow_comm': '1',
                'allow_main': '1',
                'allow_rating': '1',
                'allow_br': '1',
                'action': 'doeditnews',
                'mod': 'editnews'
            }
            self.data.update(default)

            ######### КАРТИНКИ И ССЫЛКА ЕСЛИ НА МАЛФ ###################
            error_banner = self.soup.find('input', id='xf_player_error_banner_image')
            self.data[error_banner['name']] = error_banner['value']

            error_banner_link = self.soup.find('input', id='xf_player_error_banner_link')
            self.data[error_banner_link['name']] = error_banner_link['value']
            ##############################################
    
            ####### КАТЕГОРИЯ ############
            select_category = self.soup.find('select', id='category')
            selected_category = select_category.find_all('option', selected=True)
            for option in selected_category:
                # self.data.append((select_category['name'], option['value']))
                # ЭТО СЛОВАРЬ КАК ЕСЛИ БЫ НЕТ КАЛЕНДАРЯ
                # Проверка, есть ли уже такой ключ в словаре
                if 'category[]' in self.data:
                    # Если есть, добавляем значение в список для этого ключа
                    self.data['category[]'].append(option['value'])
                else:
                    # Если ключа еще нет, создаем его и добавляем первое значение в список
                    self.data['category[]'] = [option['value']]
            #################################

            #### ID НОВОСТИ ####
            id_news = self.soup.find('input', {'name': 'id'})
            self.data[id_news['name']] = id_news['value']
            # tuple_id_news = (id_news['name'], id_news['value'])
            # self.data.append(tuple_id_news)
            #################

            #### МЕТА КЛЮЧИ ####
            meta_keywords = self.soup.find('textarea', id='keywords')
            self.data[meta_keywords['name']] = meta_keywords.text
            # tuple_meta_keywords = (meta_keywords['name'], meta_keywords.text)
            # self.data.append(tuple_meta_keywords)
            #################

            ## МЕТА ОПИСАНИЕ ####
            meta_descr = self.soup.find('input', id='autodescr')
            self.data[meta_descr['name']] = meta_descr['value']
            # tuple_meta_descr = (meta_descr['name'], meta_descr['value'])
            # self.data.append(tuple_meta_descr)
            #################

            #### МЕТА ЗАГОЛОВОК ####
            meta_title = self.soup.find('input', {'name': 'meta_title'})
            self.data[meta_title['name']] = meta_title['value']
            # tuple_meta_title = (meta_title['name'], meta_title['value'])
            # self.data.append(tuple_meta_title)
            ########################

            ### АЛЬТ НАЗВАНИЕ ####
            alt_name = self.soup.find('input', {'name': 'alt_name'})
            self.data[alt_name['name']] = alt_name['value']
            # tuple_alt_name = (alt_name['name'], alt_name['value'])
            # self.data.append(tuple_alt_name)
            #################

            #### ТОРРЕНТ ####
            torrent = self.soup.find('input', id='xf_torrent-file')
            self.data[torrent['name']] = torrent['value']
            # tuple_torrent = (torrent['name'], torrent['value'])
            # self.data.append(tuple_torrent)
            ###################

            ########## ДЕНЬ ВЫХОДА ############
            select_week_day = self.soup.find('div', id='xfield_holder_day_week').find('select')
            selected_week_day = select_week_day.find('option', selected=True)
            self.data[select_week_day['name']] = selected_week_day['value']
            # tuple_select_week_day = (select_week_day['name'], selected_week_day['value'])
            # self.data.append(tuple_select_week_day)
            #############################

            ############## СТРАНА #####################
            select_country = self.soup.find('div', id='xfield_holder_country').find('select')
            selected_country = select_country.find('option', selected=True)
            self.data[select_country['name']] = selected_country['value']
            # tuple_selected_country = (select_country['name'], selected_country['value'])
            # self.data.append(tuple_selected_country)
            ###################################

            ########### ВСЕГО СЕРИЙ #####################
            all_series = self.soup.find('input', id='xf_all_series')
            self.data[all_series['name']] = all_series['value']
            # tuple_all_series = (all_series['name'], all_series['value'])
            # self.data.append(tuple_all_series)
            ###################################

            ########### СТУДИЯ #################
            studio = self.soup.find('input', id='xf_studio')
            self.data[studio['name']] = studio['value']
            # tuple_studio = (studio['name'], studio['value'])
            # self.data.append(tuple_studio)
            ################################

            ############ ПРОДЮССЕР ###########################
            producer = self.soup.find('input', id='xf_director')
            self.data[producer['name']] = producer['value']
            # tuple_producer = (producer['name'], producer['value'])
            # self.data.append(tuple_producer)
            ###################################

            ############# ПРОДОЛЖИТЕЛЬНОСТЬ #####################
            leght_video = self.soup.find('input', id='xf_length_video')
            self.data[leght_video['name']] = leght_video['value']
            # tuple_leght_video = (leght_video['name'], leght_video['value'])
            # self.data.append(tuple_leght_video)
            ###################################


            ############# НИК ПЕРЕВОДЧИКА ####################
            name_translator = self.soup.find('input', id='xf_transfer')
            self.data[name_translator['name']] = name_translator['value']
            # tuple_name_translator = (name_translator['name'], name_translator['value'])
            # self.data.append(tuple_name_translator)
            ###################################

            ############# НИК ТАЙМЕРА ###################
            name_timming = self.soup.find('input', id='xf_timing')
            self.data[name_timming['name']] = name_timming['value']
            # tuple_name_timming = (name_timming['name'], name_timming['value'])
            # self.data.append(tuple_name_timming)
            #######################################

            ########## ТИП АНИМЕ ######################
            select_type = self.soup.find('div', id='xfield_holder_type_anime_new').find('select')
            selected_type = select_type.find('option', selected=True)
            self.data[select_type['name']] = selected_type['value']
            # tuple_select_type = (select_type['name'], selected_type['value'])
            # self.data.append(tuple_select_type)
            ###############################

            ######### СКРИНЫ СЕРИАЛА ########################
            screen = self.soup.find('input', id='xf_screen')
            self.data[screen['name']] = screen['value']
            # tuple_screen = (screen['name'], screen['value'])
            # self.data.append(tuple_screen)
            ############################

            ############ ДАТА ВЫХОДА #######################
            date_serial = self.soup.find('input', id='xf_datav')
            self.data[date_serial['name']] = date_serial['value']
            # tuple_date_serial = (date_serial['name'], date_serial['value'])
            # self.data.append(tuple_date_serial)
            ############################

            ########## ВЫБОР ГОДА #################
            select_year = self.soup.find('div', id='xfield_holder_years').find('select')
            selected_year = select_year.find('option', selected=True)
            self.data[select_year['name']] = selected_year['value']
            # tuple_select_year = (select_year['name'], selected_year['value'])
            # self.data.append(tuple_select_year)
            ##############################

            ######### ВОЗРАСТ #####################
            select_age = self.soup.find('div', id='xfield_holder_age_pg').find('select')
            selected_option = select_age.find('option', selected=True)
            self.data[select_age['name']] = selected_option['value']
            # tuple_select_age = (select_age['name'], selected_option['value'])
            # self.data.append(tuple_select_age)
            ################################

            ########## АНГЛИЙСКИЙ ТАЙТЛ ##################
            eng_title = self.soup.find('input', id='xf_eng_title')
            self.data[eng_title['name']] = eng_title['value']
            # tuple_eng_title = (eng_title['name'], eng_title['value'])
            # self.data.append(tuple_eng_title)
            ###############################

            ######## ТРЕЙЛЕР ################
            trailer = self.soup.find('input', id='xf_trailer')
            self.data[trailer['name']] = trailer['value']
            # tuple_trailer = (trailer['name'], trailer['value'])
            # self.data.append(tuple_trailer)
            ###########################

            ########### ДАББЕРЫ ####################
            dubbers = self.soup.find('input', id='xf_dubers')
            self.data[dubbers['name']] = dubbers['value']
            # tuple_dubbers = (dubbers['name'], dubbers['value'])
            # self.data.append(tuple_dubbers)
            ###############################

            ######## ПОСТЕР ##########
            poster = self.soup.find("input", id="xf_poster")
            self.data[poster['name']] = poster['value']
            # tuple_poster = (poster['name'], poster['value'])
            # self.data.append(tuple_poster)
            ##############################

            ########### СВЯЗИ #################
            svyazi = self.soup.find('textarea', id="xf_svyazi")
            self.data[svyazi['name']] = svyazi.text
            # tuple_svyazi = (svyazi["name"], svyazi.text)
            # self.data.append(tuple_svyazi)
            ####################################

            ######### ЖАНРЫ ###########
            genres = self.soup.find('input', id="xf_genres")
            self.data[genres['name']] = genres['value']
            # tuple_genres = (genres['name'], genres['value'])
            # self.data.append(tuple_genres)
            #############################

            #### ФУЛЛ СТОРИ ############
            text_full = self.soup.find('textarea', id='full_story')
            self.data[text_full['name']] = text_full.text
            # tuple_full_story = ("full_story", text_full.text)
            # self.data.append(tuple_full_story)
            ###########################

            ######## ШОРТ СТОРИ ##########
            text_short = self.soup.find('textarea', id='short_story')
            self.data[text_short['name']] = text_short.text
            # tuple_short_story = ("short_story", text_short.text)
            # self.data.append(tuple_short_story)
            #############################

            ### ЗАГОЛОВОК #########
            title_input = self.soup.find('input', {'name': 'title'})
            self.data[title_input['name']] = title_input['value']
            # title_tuple = ('title', title_input['value'])
            # self.data.append(title_tuple)
            ########################
            return True
        # except Exception as e:
        #     log_config.setup_logger().exception(e)
        #     return None
    
    def get_list_series(self, url:str) -> list:
        req = self.session.get(url, headers=self.headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        series = soup.find_all('div', class_='extra-series-item')
        data = []
        for div in series:
            data_frame = div['data-iframe']
            text = div.get_text(strip=True)
            data.append((data_frame, text))
        return data

  
# if __name__ == '__main__':
#     ParseMaunt().update_seria_maunt(r"https://animaunt.org/%E7%A7%81%E3%81%AF%E7%8B%AC%E8%BA%AB%E3%81%A7%E3%81%99.php?mod=editnews&action=editnews&id=12789", '6')