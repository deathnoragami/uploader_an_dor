from PyQt5.QtWidgets import QDialog, QMessageBox
from .autorizationUI import Ui_authorization_app
from connect_firebase import Connect
from ui import Ui_MainWindow
from config import Config as cfg

import os

class AuthorizationApp():
    def __init__(self):
        super(AuthorizationApp, self).__init__()
        self.db = Connect()
        widget = QDialog()
        self.auto_ui = Ui_authorization_app()
        self.auto_ui.setupUi(widget)
        
        if self.db.find_user_uid(cfg().get_uid_program()) != None:
            self.auto_ui.line_login.setDisabled(True)
            self.auto_ui.line_pass.setDisabled(True)
            self.auto_ui.btn_autorizade.setText('Авторизован')
            self.auto_ui.btn_autorizade.setDisabled(True)
        else:
            self.auto_ui.btn_autorizade.clicked.connect(self.authenticate)
        
        widget.rejected.connect(self.db.close)
        widget.exec_()        


    def authenticate(self):
        found_user = None
        try:
            users = self.db.get_user_data()
            for user in users:
                if user:
                    if user["name"] == self.auto_ui.line_login.text() and user["pass"] == self.auto_ui.line_pass.text():
                        found_user = user
                        cfg().set_uid_program(found_user["uid"])
                        self.auto_ui.btn_autorizade.setText('Авторизован')
                        self.auto_ui.btn_autorizade.setDisabled(True)
                        QMessageBox.information(None, "Авторизация успех!", "Вы успешно авторизовались, перезапустите программу.")
                        break
            if found_user is None:
                QMessageBox.information(None, "Авторизация!", "Пользователь был не найден или логин и пароль не верный.")
        except Exception as e:
            print(e)
            

        
        

