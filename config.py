import configparser
import os



class Config():
    def __init__(self):
        self.cfg = configparser.ConfigParser()
        if not os.path.exists('assets'):
            os.makedirs('assets')
        if os.path.exists('assets/config.ini') == False:
            self.cfg['GLOBAL'] = {}
            self.cfg['GLOBAL']['id_chat'] = ''
            self.cfg['GLOBAL']['defoult_path_pic_anime'] = ''
            self.cfg['GLOBAL']['defoult_path_video_anime'] = ''
            self.cfg['GLOBAL']['defoult_path_pic_dorama'] = ''
            self.cfg['GLOBAL']['defoult_path_video_dorama'] = ''
            self.cfg['USER'] = {}
            self.cfg['USER']['uid_program'] = ''
            self.cfg['USER']['vk_token'] = ''
            self.cfg['USER']['email_hent'] = ''
            self.cfg['USER']['api_hent'] = ''
            self.cfg['USER']['user_maunt'] = ''
            self.cfg['USER']['pass_maunt'] = ''
            self.cfg['USER']['user_malf'] = ''
            self.cfg['USER']['pass_malf'] = ''
            self.cfg["USER"]['a_site_login'] = ''
            self.cfg["USER"]['a_site_pass'] = ''
            self.cfg["USER"]['m_site_login'] = ''
            self.cfg["USER"]['m_site_pass'] = ''
            with open('assets/config.ini', 'w') as configfile:
                self.cfg.write(configfile)
        else:
            config = configparser.ConfigParser()
            config.read('assets/config.ini')
            for section in ['USER']:
                for option in ['uid_program', 'vk_token', 'email_hent', 'api_hent', 'user_maunt', 'pass_maunt', 'user_malf', 'pass_malf', 'a_site_login', 'a_site_pass', 'm_site_login', 'm_site_pass']:
                    if option not in config[section]:
                        config[section][option] = ''
            with open('assets/config.ini', 'w') as configfile:
                config.write(configfile)
        self.cfg.read('assets/config.ini')
    
    def get_id_chat(self):
        return self.cfg['GLOBAL']['id_chat']
    
    def get_defoult_path_pic_anime(self):
        return self.cfg['GLOBAL']['defoult_path_pic_anime']
    
    def get_defoult_path_video_anime(self):
        return self.cfg['GLOBAL']['defoult_path_video_anime']
    
    def get_defoult_path_pic_dorama(self):
        return self.cfg['GLOBAL']['defoult_path_pic_dorama']
    
    def get_defoult_path_video_dorama(self):
        return self.cfg['GLOBAL']['defoult_path_video_dorama']

    def get_uid_program(self):
        return self.cfg['USER']['uid_program']
    
    def get_vk_token(self):
        return self.cfg['USER']['vk_token']
    
    def get_email_hent(self):
        return self.cfg['USER']['email_hent']

    def get_api_hent(self):
        return self.cfg['USER']['api_hent']
    
    def get_info_maunt(self):
        return [self.cfg['USER']['user_maunt'], self.cfg['USER']['pass_maunt']]

    def get_info_malf(self):
        return [self.cfg['USER']['user_malf'], self.cfg['USER']['pass_malf']]
    
    def get_a_info_site(self):
        return [self.cfg['USER']['a_site_login'], self.cfg['USER']['a_site_pass']]
    
    def get_m_info_site(self):
        return [self.cfg['USER']['m_site_login'], self.cfg['USER']['m_site_pass']]

    def set_id_chat(self, id_chat):
        self.cfg['GLOBAL']['id_chat'] = id_chat
        with open('assets/config.ini', 'w') as configfile:
            self.cfg.write(configfile)

    def set_email_hent(self, email):
        self.cfg['USER']['email_hent'] = email
        with open('assets/config.ini', 'w') as configfile:
            self.cfg.write(configfile)

    def set_api_hent(self, api):
        self.cfg['USER']['api_hent'] = api
        with open('assets/config.ini', 'w') as configfile:
            self.cfg.write(configfile)
    
    def set_defoult_path_pic_anime(self, path):
        self.cfg['GLOBAL']['defoult_path_pic_anime'] = path
        with open('assets/config.ini', 'w') as configfile:
            self.cfg.write(configfile)

    def set_defoult_path_video_anime(self, path):
        self.cfg['GLOBAL']['defoult_path_video_anime'] = path
        with open('assets/config.ini', 'w') as configfile:
            self.cfg.write(configfile)
            
    def set_defoult_path_pic_dorama(self, path):
        self.cfg['GLOBAL']['defoult_path_pic_dorama'] = path
        with open('assets/config.ini', 'w') as configfile:
            self.cfg.write(configfile)
            
    def set_defoult_path_video_dorama(self, path):
        self.cfg['GLOBAL']['defoult_path_video_dorama'] = path
        with open('assets/config.ini', 'w') as configfile:
            self.cfg.write(configfile)
            
    def set_uid_program(self, uid_program):
        self.cfg['USER']['uid_program'] = uid_program
        with open('assets/config.ini', 'w') as configfile:
            self.cfg.write(configfile)
            
    def set_vk_token(self, vk_token):
        self.cfg['USER']['vk_token'] = vk_token
        with open('assets/config.ini', 'w') as configfile:
            self.cfg.write(configfile)

    def set_info_maunt(self, user_maunt, pass_maunt):
        self.cfg['USER']['user_maunt'] = user_maunt
        self.cfg['USER']['pass_maunt'] = pass_maunt
        with open('assets/config.ini', 'w') as configfile:
            self.cfg.write(configfile)

    def set_info_malf(self, user_malf, pass_malf):
        self.cfg['USER']['user_malf'] = user_malf
        self.cfg['USER']['pass_malf'] = pass_malf
        with open('assets/config.ini', 'w') as configfile:
            self.cfg.write(configfile)
            
    def set_a_info_site(self, login, pasw):
        self.cfg['USER']['a_site_login'] = login
        self.cfg['USER']['a_site_pass'] = pasw
        with open('assets/config.ini', 'w') as configfile:
            self.cfg.write(configfile)
            
    def set_m_info_site(self, login, pasw):
        self.cfg['USER']['m_site_login'] = login
        self.cfg['USER']['m_site_pass'] = pasw
        with open('assets/config.ini', 'w') as configfile:
            self.cfg.write(configfile)
        