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
            
            with open('assets/config.ini', 'w') as configfile:
                self.cfg.write(configfile)
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