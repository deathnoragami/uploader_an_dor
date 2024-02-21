from PyQt5.QtWidgets import QDialog, QMessageBox
from .autorizationUI import Ui_authorization_tg
import os
from pyrogram import Client, errors


class AuthorizationTG():
    def __init__(self):
        super(AuthorizationTG, self).__init__()
        widget = QDialog()
        self.auto_ui = Ui_authorization_tg()
        self.auto_ui.setupUi(widget)
        
        if os.path.exists('assets/my_session_tg.session'):
            self.auto_ui.btn_give_code.setDisabled(True)
            self.auto_ui.btn_give_code.setText('Авторизован')
            self.auto_ui.btn_autorization.setHidden(True)
            self.auto_ui.line_number_phone.setDisabled(True)
        else:
            self.auto_ui.btn_give_code.clicked.connect(self.send_code)
            self.auto_ui.btn_autorization.clicked.connect(self.autorization)
        
        widget.exec_()
        
    
    def send_code(self):
        if self.auto_ui.line_number_phone.text():
            self.number_phone = self.auto_ui.line_number_phone.text()
            api_id = int(os.getenv("API_ID"))
            api_hash = os.getenv("API_HASH")
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
                self.client.stop()
        else:
            QMessageBox.warning(None, "Ошибка", "Не введен номер телефона")


    def autorization(self):
        fine_autho = False
        if self.number_phone and self.auto_ui.line_code.text():
            try:
                self.client.sign_in(phone_number=self.number_phone, 
                                    phone_code_hash=self.send_code_info.phone_code_hash, 
                                    phone_code=self.auto_ui.line_code.text())
                fine_autho = True
            except errors.PhoneCodeInvalid:
                QMessageBox.warning(None, "Ошибка", "Неверный код")
            except errors.PhoneCodeExpired:
                QMessageBox.warning(None, "Ошибка", "Код истек")
            except errors.exceptions.unauthorized_401.SessionPasswordNeeded:
                self.client.check_password(self.auto_ui.line_password.text())
                fine_autho = True
            if fine_autho:
                self.auto_ui.line_password.setDisabled(True)
                self.auto_ui.btn_autorization.setText('Авторизован')
                self.auto_ui.btn_give_code.setDisabled(True)
                self.auto_ui.line_number_phone.setDisabled(True)
                self.auto_ui.line_code.setDisabled(True)
        else:
            QMessageBox.warning(None, "Ошибка", "Не введен код")
            