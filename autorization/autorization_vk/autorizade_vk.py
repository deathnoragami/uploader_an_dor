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
        res = requests.get(f'https://api.vk.com/method/users.get?access_token={token}&v=5.199')
        if res.status_code == 200:
            response_json = res.json()
            if "error" in response_json:
                error_message = response_json["error"]["error_msg"]
                print(error_message)
            else:
                self.auto_ui.line_token_vk.setDisabled(True)
                self.auto_ui.btn_autho_vk.setText('Авторизован')
                self.auto_ui.btn_autho_vk.setDisabled(True)
        self.auto_ui.btn_autho_vk.clicked.connect(self.autorization)
        
        widget.exec_()
        
        
    def autorization(self):
        vk_token = self.auto_ui.line_token_vk.text()
        if vk_token:
            try:
                vk_token = vk_token.split('&')[0].split('=')[1]
            except:
                pass
            res = requests.get(f'https://api.vk.com/method/users.get?access_token={vk_token}&v=5.199')
            if res.status_code == 200:
                response_json = res.json()
                if "error" in response_json:
                    print('неверный токен')
                else:
                    Config().set_vk_token(vk_token)
                    self.auto_ui.line_token_vk.setDisabled(True)
                    self.auto_ui.btn_autho_vk.setText('Авторизован')
                    return True
        else:
            print('не введен токен') # TODO : вывести
            