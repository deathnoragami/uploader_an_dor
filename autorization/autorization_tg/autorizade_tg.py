from PyQt5.QtWidgets import QDialog
from .autorizationUI import Ui_authorization_tg
import os
from pyrogram import Client


class AuthorizationTG():
    def __init__(self):
        super(AuthorizationTG, self).__init__()
        widget = QDialog()
        self.auto_ui = Ui_authorization_tg()
        self.auto_ui.setupUi(widget)
        
        if os.path.exists('assets/my_session_tg.session'):
            self.auto_ui.btn_give_code.setDisabled(True)
            self.auto_ui.btn_give_code.setText('Авторизован')
            self.auto_ui.line_number_phone.setDisabled(True)
        else:
            self.auto_ui.btn_give_code.clicked.connect(self.send_code)
            self.auto_ui.btn_autorization.clicked.connect(self.autorization)
        
        widget.exec_()
        
    
    def send_code(self):
        self.number_phone = self.auto_ui.line_number_phone.text()
        api_id = 22207760 # TODO : переместить в env
        api_hash = '399b1653a041f35af2d2774e9b74656a'
        self.client = Client('assets/my_session_tg', api_id, api_hash)
        self.client.connect()
        try:
            self.send_code_info = self.client.send_code(self.number_phone)
            self.auto_ui.btn_give_code.setDisabled(True)
            self.auto_ui.line_number_phone.setDisabled(True)
            self.auto_ui.line_code.setDisabled(False)
            self.auto_ui.btn_autorization.setDisabled(False)
            self.auto_ui.line_password.setDisabled(False)
            return self.send_code_info, self.client, self.number_phone
        except Exception as e:
            print(e)
            self.client.__exit__()


    def autorization(self):
        try:
            self.client.sign_in(phone_number=self.number_phone, 
                                phone_code_hash=self.send_code_info.phone_code_hash, 
                                phone_code=self.auto_ui.line_code.text())
        except:
            self.client.check_password(self.auto_ui.line_password.text())
            self.client.__exit__()
            
        
        self.client.__exit__()