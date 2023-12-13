from PyQt5.QtWidgets import QDialog
from .autorizationUI import Ui_authorization_app
from connect_firebase import Connect
import os

class AuthorizationApp():
    def __init__(self):
        super(AuthorizationApp, self).__init__()
        self.db = Connect()
        widget = QDialog()
        self.auto_ui = Ui_authorization_app()
        self.auto_ui.setupUi(widget)
        
        if os.path.exists('assets/session_timmers'):
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
        for user in self.db.get_user_data():
            if user:
                if user["name"] == self.auto_ui.line_login.text() and user["pass"] == self.auto_ui.line_pass.text():
                    found_user = user
                    if not os.path.exists("assets"):
                        os.makedirs("assets")
                    with open('assets/session_timmers', 'w+') as file:
                        file.write(str(found_user['uid']))
                    self.auto_ui.btn_autorizade.setText('Авторизован')
                    self.auto_ui.btn_autorizade.setDisabled(True)
                    break
        if found_user is None:
            print('nety')
            ... # TODO : пользователь не найден
            

        
        

