from PyQt5.QtWidgets import QDialog
from .autorizationUI import Ui_authorization_vk
import os
import requests

class AuthorizationVK():
    def __init__(self):
        super(AuthorizationVK, self).__init__()
        widget = QDialog()
        self.auto_ui = Ui_authorization_vk()
        self.auto_ui.setupUi(widget)
        
        if os.path.exists('assets/my_session_vk'):
            self.auto_ui.line_token_vk.setDisabled(True)
            self.auto_ui.btn_autho_vk.setText('Авторизован')
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
            response = requests.get(f'https://api.vk.com/method/users.get?access_token={vk_token}&v=5.131')
            if response.status_code == 200 and 'error' not in response.json():
                if not os.path.exists("assets"):
                    os.makedirs("assets")
                with open('assets/my_session_vk', 'w+') as file:
                    file.write(f"{vk_token}")
                    self.auto_ui.line_token_vk.setDisabled(True)
                    self.auto_ui.btn_autho_vk.setText('Авторизован')
            else:
                print('неверный токен') # TODO : вывести
        else:
            print('не введен токен') # TODO : вывести
            