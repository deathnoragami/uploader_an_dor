from PyQt5.QtWidgets import QApplication, QMainWindow
from autorizationUI import AutorizationUI
from app import MainWindow
from connect_firebase import Connect
import sys
import os

class AuthorizationWindow(QMainWindow):
    def __init__(self, app):
        super(AuthorizationWindow, self).__init__()
        self.ui = AutorizationUI()
        self.ui.setupUi(self)
        
        self.ui.btn_autorizade.clicked.connect(self.authenticate)
        self.app = app

    def authenticate(self):
        db = Connect()
        found_user = None
        for user in db.get_user_data():
            if user:
                if user["name"] == self.ui.line_login.text() and user["pass"] == self.ui.line_pass.text():
                    found_user = user
                    if not os.path.exists("assets"):
                        os.makedirs("assets")
                    with open('assets/session_timmers', 'w+') as file:
                        file.write(str(found_user['uid']))
                    break
        if not found_user:
            ... # TODO : пользователь не найден

            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    authorization_window = AuthorizationWindow(app)
    authorization_window.show()
    sys.exit(app.exec_())