from PyQt5.QtWidgets import QDialog, QMessageBox
from .UI_sites import Ui_Form
from config import Config

import pysftp
import os
import log_config
import requests
import fake_useragent
from bs4 import BeautifulSoup


class AutorizationSites():
    def __init__(self):
        super(AutorizationSites, self).__init__()
        widget = QDialog()
        self.auto_ui = Ui_Form()
        self.auto_ui.setupUi(widget)
        self.auto_ui.btn_auto_animaunt.clicked.connect(self.login_animaunt)
        self.auto_ui.btn_auto_malf.clicked.connect(self.login_malfurik)
        self.auto_ui.lineEdit.setText(Config().get_a_info_site()[0])
        self.auto_ui.lineEdit_2.setText(Config().get_a_info_site()[1])
        self.auto_ui.lineEdit_4.setText(Config().get_m_info_site()[0])
        self.auto_ui.lineEdit_3.setText(Config().get_m_info_site()[1])
            
        widget.exec_()
        
    def login_animaunt(self):
        login = self.auto_ui.lineEdit.text()
        pasw = self.auto_ui.lineEdit_2.text()
        user = fake_useragent.UserAgent().random
        headers = {
            'user-agent' : user
        }
        data = {
            'subaction': 'dologin',
            'username': login,
            'password': pasw,
            'selected_language': 'Russian',
        }
        auth = requests.post(r'https://animaunt.org/私は独身です.php?mod=main', headers=headers, data=data)
        if 'Неверно введены данные для входа!' in auth.text:
            QMessageBox.warning(None, "Авторизация", "Не правильный логин или пароль.")
        else:
            self.auto_ui.btn_auto_animaunt.setDisabled(True)
            self.auto_ui.btn_auto_animaunt.setText("Войден")
            Config().set_a_info_site(login, pasw)
        
    def login_malfurik(self):
        login = self.auto_ui.lineEdit_4.text()
        pasw = self.auto_ui.lineEdit_3.text()
        session = requests.Session()
        user = fake_useragent.UserAgent().random
        headers = {
            'user-agent' : user
        }
        cookies = {
            'wpdiscuz_hide_bubble_hint': '1',
            'wp-settings-870': 'libraryContent%3Dbrowse%26posts_list_mode%3Dlist',
            'wordpress_test_cookie': r'WP%20Cookie%20check',
        }
        data = {
            'log': login,
            'pwd': pasw,
            'wp-submit': 'Войти',
            'redirect_to': 'https://anime.malfurik.online/wp-admin/',
            'testcookie': '1',
        }
        auth = session.post('https://anime.malfurik.online/wp-login.php', headers=headers, cookies=cookies, data=data)
        soup = BeautifulSoup(auth.content, 'html.parser')
        login_error_div = soup.find('div', id='login_error')
        if login_error_div:
            QMessageBox.warning(None, "Авторизация", "Не правильный логин или пароль.")
        else:
            self.auto_ui.btn_auto_malf.setDisabled(True)
            self.auto_ui.btn_auto_malf.setText("Войден")
            Config().set_m_info_site(login, pasw)