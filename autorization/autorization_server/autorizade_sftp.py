from PyQt5.QtWidgets import QDialog, QMessageBox
from .autorizationUI import Ui_autorization_server
from connect_firebase import Connect

import pysftp
import os


class AutorizationServer():
    def __init__(self):
        super(AutorizationServer, self).__init__()
        widget = QDialog()
        self.auto_ui = Ui_autorization_server()
        self.auto_ui.setupUi(widget)

        self.auto_ui.btn_enter_malfurik.clicked.connect(self.add_malfurik)
        self.auto_ui.btn_enter_animaunt.clicked.connect(self.add_animaunt)
        
        file_path = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "../assets/session_timmers"))
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                uid = file.read()
                print(uid)
            db = Connect()
            user_data = db.find_user_uid(uid)
            db.close()
            if user_data:
                if all(key in user_data and user_data[key] for key in ['malf_pass', 'malf_login', 'maunt_login', 'maunt_pass']):
                    self.auto_ui.animaunt_login.setDisabled(True)
                    self.auto_ui.pass_animaunt.setDisabled(True)
                    self.auto_ui.login_malfurik.setDisabled(True)
                    self.auto_ui.pass_malfurik.setDisabled(True)
                    self.auto_ui.btn_enter_animaunt.setDisabled(True)
                    self.auto_ui.btn_enter_animaunt.setText('Авторизован')
                    self.auto_ui.btn_enter_malfurik.setDisabled(True)
                    self.auto_ui.btn_enter_malfurik.setText('Авторизован')
                else:
                    print(user_data)
                    if ('malf_pass' not in user_data or not user_data['malf_pass']) or ('malf_login' not in user_data or not user_data['malf_login']):
                        self.auto_ui.animaunt_login.setDisabled(True)
                        self.auto_ui.pass_animaunt.setDisabled(True)
                        self.auto_ui.btn_enter_animaunt.setDisabled(True)
                        self.auto_ui.btn_enter_animaunt.setText('Авторизован')
                    if ('maunt_login' not in user_data or not user_data['maunt_login']) or ('maunt_pass' not in user_data or not user_data['maunt_pass']):
                        self.auto_ui.login_malfurik.setDisabled(True)
                        self.auto_ui.pass_malfurik.setDisabled(True)
                        self.auto_ui.btn_enter_malfurik.setDisabled(True)
                        self.auto_ui.btn_enter_malfurik.setText('Авторизован')

        widget.exec_()
        
        
    def add_malfurik(self):
        login_malf = self.auto_ui.login_malfurik.text()
        pass_malf = self.auto_ui.pass_malfurik.text()
        if login_malf and pass_malf:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            try:
                with pysftp.Connection(host='95.217.32.176',
                                       port=22,
                                       username=login_malf, 
                                       password=pass_malf, 
                                       cnopts=cnopts) as sftp:
                    self.auto_ui.btn_enter_malfurik.setDisabled(True)
                    self.auto_ui.btn_enter_malfurik.setText('Авторизован')
                    self.auto_ui.login_malfurik.setDisabled(True)
                    self.auto_ui.pass_malfurik.setDisabled(True)
                    with open('assets/session_timmers', 'r') as file:
                        uid = file.read()
                        self.db = Connect()
                        self.db.update_malf_data(uid, login_malf, pass_malf)
                        self.db.close()
            except pysftp.AuthenticationException:
                QMessageBox.warning(None, "Ошибка", "Неверный логин или пароль")
            except Exception as e:
                QMessageBox.warning(None, "Ошибка", f"Ошибка подключения, {str(e)}")


    def add_animaunt(self):
        login_maunt = self.auto_ui.animaunt_login.text()
        pass_maunt = self.auto_ui.pass_animaunt.text()
        if login_maunt and pass_maunt:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            try:
                with pysftp.Connection(host='176.9.123.231',
                                       port=22,
                                       username=login_maunt, 
                                       password=pass_maunt, 
                                       cnopts=cnopts) as sftp:
                    self.auto_ui.btn_enter_animaunt.setDisabled(True)
                    self.auto_ui.btn_enter_animaunt.setText('Авторизован')
                    self.auto_ui.animaunt_login.setDisabled(True)
                    self.auto_ui.pass_animaunt.setDisabled(True)
                    with open('assets/session_timmers', 'r') as file:
                        uid = file.read()
                        self.db = Connect()
                        self.db.update_maunt_data(uid, login_maunt, pass_maunt)
                        self.db.close()
            except pysftp.AuthenticationException:
                QMessageBox.warning(None, "Ошибка", "Неверный логин или пароль")
            except Exception as e:
                QMessageBox.warning(None, "Ошибка", f"Ошибка подключения, {str(e)}")


