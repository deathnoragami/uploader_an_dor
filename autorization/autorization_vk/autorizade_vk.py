from PyQt5.QtWidgets import QDialog
from .autorizationUI import Ui_authorization_vk
import os
import requests
from config import Config

class AuthorizationVK():
    def __init__(self):
        super(AuthorizationVK, self).__init__()
        widget = QDialog()
        self.auto_ui = Ui_authorization_vk()
        self.auto_ui.setupUi(widget)
        
        token = Config().get_vk_token()
        res = requests.get('https://api.vk.com/method/users.get?access_token={token}&v=5.199')
        if res.status_code == 200:
            self.auto_ui.line_token_vk.setDisabled(True)
            self.auto_ui.btn_autho_vk.setText('Авторизован')
            self.auto_ui.btn_autho_vk.setDisabled(True)
        else:
            self.auto_ui.btn_autho_vk.clicked.connect(self.autorization)
        
        widget.exec_()
        
        
    def autorization(self):
        vk_token = self.auto_ui.line_token_vk.text()
        if vk_token:
            try:
                vk_token = vk_token.split('&')[0].split('=')[1]
            except:
                pass
            response = requests.get(f'https://api.vk.com/method/users.get?access_token={vk_token}&v=5.199')
            if response.status_code == 200:
                Config().set_vk_token(vk_token)
                self.auto_ui.line_token_vk.setDisabled(True)
                self.auto_ui.btn_autho_vk.setText('Авторизован')
            else:
                print('неверный токен') # TODO : вывести
        else:
            print('не введен токен') # TODO : вывести
            