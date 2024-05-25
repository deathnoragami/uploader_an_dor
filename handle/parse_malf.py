import requests
import fake_useragent
from bs4 import BeautifulSoup
import re
import sys
from datetime import datetime, timedelta
from config import Config
from typing import Optional, List

class ParseMalf:
    def __init__(self) -> None:
        super().__init__()
        self.session = requests.Session()
        user = fake_useragent.UserAgent().random
        self.headers = {
            'user-agent' : user
        }
        
    def update_seria_malf(
        self,
        link: str,
        timming_list: Optional[List] = None,
        name_file: Optional[str] = None,
    ) -> bool | None:
        """
        Updates a serial on Malfurik website.

        Args:
            link (str): The link to the serial's page on the website.
            timming_list (Optional[List[]): The list of timecodes for the video links.
                If not provided, will be None.
            name_file (Optional[str]): The name of the file to be uploaded.
                If not provided, will be None.

        Returns:
            None
        """
        if self.autorization_malfurik(link):
            self.data = [
                ('_wp_http_referer', self.soup.find('input', {'name': '_wp_http_referer'})['value']),
                ('user_ID', self.soup.find('input', id='user-id')['value']),
                ('action', self.soup.find('input', id='hiddenaction')['value']),
                ('originalaction', self.soup.find('input', id='originalaction')['value']),
                ('post_author', self.soup.find('input', id='post_author')['value']),
                ('post_type', self.soup.find('input', id='post_type')['value']),
                ('original_post_status', self.soup.find('input', id='original_post_status')['value']),
                ('referredby', 'https://anime.malfurik.online/wp-admin/edit.php?post_type=movie'),
                ('_wp_original_http_referer', 'https://anime.malfurik.online/wp-admin/edit.php?post_type=movie'),
                ('post_ID', self.soup.find('input', id='post_ID')['value']),
                ('hidden_post_status', 'publish'),
                ('post_status', 'publish'),
                ('hidden_post_visibility', 'public'),
                ('visibility', 'public'),
                ('original_publish', 'Обновить'),
                ('save', 'Обновить'),
            ]
            self.get_token()
            self.video_links(time_codes=timming_list, name_file=name_file)
            self.dont_change()
            ps = self.session.post(
                'https://anime.malfurik.online/wp-admin/post.php', headers=self.headers, data=self.data
            )
            ps = self.session.post('https://anime.malfurik.online/wp-admin/post.php', headers=self.headers, data=self.data)
            if ps.status_code == 200:
                return True
            else:
                return None
        else:
            return None

        
    def autorization_malfurik(self, link):
        data = Config().get_m_info_site()
        cookies = {
            'wpdiscuz_hide_bubble_hint': '1',
            'wp-settings-870': 'libraryContent%3Dbrowse%26posts_list_mode%3Dlist',
            'wordpress_test_cookie': r'WP%20Cookie%20check',
            }
        data = {
            'log': data[0],
            'pwd': data[1],
            'wp-submit': 'Войти',
            'redirect_to': 'https://anime.malfurik.online/wp-admin/',
            'testcookie': '1',
            }
        auth = self.session.post('https://anime.malfurik.online/wp-login.php', headers=self.headers, cookies=cookies, data=data)
        soup_auth = BeautifulSoup(auth.content, 'html.parser')
        login_error_div = soup_auth.find('div', id='login_error')
        if login_error_div:
            pass
        else:
            res = self.session.get(link, headers=self.headers)
            self.soup =  BeautifulSoup(res.text, 'html.parser')
            return True
            

    def video_links(self, name_file, time_codes):
        ########### ПЛЕЕЕР ТАЙМИНГИ ############
        titles_video = self.soup.find_all('input', id=re.compile('^themeum_video_info_title'))
        for title_name in titles_video:
            self.data.append((title_name['name'], title_name['value']))
            name_attr = title_name['name'].replace("[themeum_video_info_title]", "")
            self.data.append((f'{name_attr}[themeum_video_source]', 'self'))
            last_video_link = self.soup.find('input', {'name': f'{name_attr}[themeum_video_link]'})['value']
            self.data.append((f'{name_attr}[themeum_video_link]', last_video_link))
            name_code = re.compile(f'{re.escape(name_attr)}\[themeum_timecodes\]\[\d+\]')
            time_code = self.soup.find_all('input', {'name': name_code})
            for time in time_code:
                if 'value' in time.attrs:
                    self.data.append((time['name'], time['value']))
        ###########################################
        number = re.findall(r'\d+', name_attr)[0]
        new_number = int(number) + 1
        name_attr = f'themeum_movie_trailer_info[{new_number}]'
        
        source_video = (f'{name_attr}[themeum_video_source]', 'self')
        if name_file:
            new_video_link = last_video_link.rsplit("/", 1)[0] + "/" + name_file
            old_s_number = title_name['value'].split()[0]
            new_s_number = str(int(old_s_number) + 1)
            title = (f'{name_attr}[themeum_video_info_title]', f'{new_s_number} серия')
            video_link = (f'{name_attr}[themeum_video_link]', new_video_link)
        else:
            string = last_video_link.split("/")[-1]
            pattern = r'(\d+).*x*.mp4'
            match = re.search(pattern, string)
            number = int(match.group(1)) + 1
            new_string = re.sub(pattern, f"{number:02d}", string)
            new_video_link = last_video_link.rsplit("/", 1)[0] + "/" + new_string + 'x.mp4'
            video_link = (f'{name_attr}[themeum_video_link]', new_video_link)
            title = (f'{name_attr}[themeum_video_info_title]', f'{number} серия')
        self.data.append(title)
        self.data.append(source_video)
        self.data.append(video_link)
        if time_codes:
            time_code = [(f'{name_attr}[themeum_timecodes][{i}]', time) for i, time in enumerate(time_codes)]
            for item in time_code:
                self.data.append(item)
        
    
    def get_token(self):    
        ###### TOKEN ##################
        input_closedpostboxesnonce = self.soup.find('input', id='closedpostboxesnonce')
        self.data.append((input_closedpostboxesnonce['name'], input_closedpostboxesnonce['value']))

        input_meta_box_order_nonce = self.soup.find('input', id='meta-box-order-nonce')
        self.data.append((input_meta_box_order_nonce['name'], input_meta_box_order_nonce['value']))

        input__wpnonce = self.soup.find('input', id='_wpnonce')
        self.data.append((input__wpnonce['name'], input__wpnonce['value']))

        samplepermalinknonce = self.soup.find('input', id='samplepermalinknonce')
        self.data.append((samplepermalinknonce['name'], samplepermalinknonce['value']))

        act_div = self.soup.find('div', id='acf-form-data')
        act_inputs = act_div.find_all('input')
        for input in act_inputs:
            self.data.append((input['name'], input['value']))

        input_pvc_nonce = self.soup.find('input', id='pvc_nonce')
        self.data.append((input_pvc_nonce['name'], input_pvc_nonce['value']))

        input__ajax_nonce_add_movie_cat = self.soup.find('input', id='_ajax_nonce-add-movie_cat')
        self.data.append((input__ajax_nonce_add_movie_cat['name'], input__ajax_nonce_add_movie_cat['value']))

        input_nonce_video_post_meta = self.soup.find('input', id='nonce_video-post-meta')
        self.data.append((input_nonce_video_post_meta['name'], input_nonce_video_post_meta['value']))

        input_yoast_free_metabox_nonce = self.soup.find('input', id='yoast_free_metabox_nonce')
        self.data.append((input_yoast_free_metabox_nonce['name'], input_yoast_free_metabox_nonce['value']))

        input_yoast_wpseo_primary_movie_cat_nonce = self.soup.find('input', id='yoast_wpseo_primary_movie_cat_nonce')
        self.data.append((input_yoast_wpseo_primary_movie_cat_nonce['name'], input_yoast_wpseo_primary_movie_cat_nonce['value']))

        input_add_comment_nonce = self.soup.find('input', id='add_comment_nonce')
        self.data.append((input_add_comment_nonce['name'], input_add_comment_nonce['value']))

        input__ajax_fetch_list_nonce = self.soup.find('input', id='_ajax_fetch_list_nonce')
        self.data.append((input__ajax_fetch_list_nonce['name'], input__ajax_fetch_list_nonce['value']))
        #############################################
        
    def dont_change(self):
        post_title = self.soup.find('input', id='title')
        self.data.append((post_title['name'], post_title['value']))

        input_content = self.soup.find('textarea', id='content')
        self.data.append((input_content['name'], input_content.text))

        category = self.soup.find_all('input', {'name': 'tax_input[movie_cat][]', 'checked': 'checked'})
        for cat in category:
            self.data.append((cat['name'], cat['value']))

        input_thumb = self.soup.find('input', id='_thumbnail_id')
        self.data.append((input_thumb['name'], input_thumb['value']))

        select_genre = self.soup.find('select', id='janr')
        option_genre = select_genre.find('option', selected=True)
        self.data.append((select_genre['name'], option_genre['value']))

        input_novinka = self.soup.find('input', id='novinka')
        self.data.append((input_novinka['name'], input_novinka['value']))

        input_pinned_title = self.soup.find('input', id='pinned_title')
        self.data.append((input_pinned_title['name'], input_pinned_title['value']))

        input_themeum_movie_release_year = self.soup.find('input', id='themeum_movie_release_year')
        if input_themeum_movie_release_year.has_attr('value'):
            self.data.append((input_themeum_movie_release_year['name'], input_themeum_movie_release_year['value']))

        input_themeum_movie_original_name = self.soup.find('input', id='themeum_movie_original_name')
        if input_themeum_movie_original_name.has_attr('value'):
            self.data.append((input_themeum_movie_original_name['name'], input_themeum_movie_original_name['value']))

        input_themeum_movie_director = self.soup.find('input', id='themeum_movie_director')
        if input_themeum_movie_director.has_attr('value'):
            self.data.append((input_themeum_movie_director['name'], input_themeum_movie_director['value']))

        input_themeum_movie_epizod = self.soup.find('input', id='themeum_movie_epizod')
        if input_themeum_movie_epizod.has_attr('value'):
            self.data.append((input_themeum_movie_epizod['name'], input_themeum_movie_epizod['value']))

        select_age = self.soup.find('select', id='age')
        option_age = select_age.find('option', selected=True)['value']
        self.data.append((select_age['name'], option_age))

        input_studio = self.soup.find('input', id='studio2')
        if input_studio.has_attr('value'):
            self.data.append((input_studio['name'], input_studio['value']))

        input_country = self.soup.find('input', id='country')
        if input_country.has_attr('value'):
            self.data.append((input_country['name'], input_country['value']))

        input_actor = self.soup.find_all('input', id=re.compile('^actors'))
        for actor in input_actor:
            self.data.append((actor['name'], actor['value']))

        input_advanced_view = self.soup.find('input', {'name': 'advanced_view'})
        if input_advanced_view.has_attr('checked'):
            self.data.append((input_advanced_view['name'], input_advanced_view['value']))

        input_comment_status = self.soup.find('input', id='comment_status')
        self.data.append((input_comment_status['name'], input_comment_status['value']))

        input_post_name = self.soup.find('input', id='post_name')
        self.data.append((input_post_name['name'], input_post_name['value']))

    def get_list_series(self, url:str) -> list:
        req = self.session.get(url, headers=self.headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        options = soup.select('select[name="pmovie__select-items"] option')
        data = []
        for option in options:
            series_number = option.get_text(strip=True)
            video_url = 'https://video.malfurik.online/mp4/' + '/'.join(option['value'].split('/')[6:])
            data.append((series_number, video_url))
        return data