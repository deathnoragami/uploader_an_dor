from PyQt5.QtWidgets import QDialog, QMessageBox
from .autorizationUI import Ui_autorization_server
from config import Config

import pysftp
import os
import log_config


class AutorizationServer():
    def __init__(self):
        super(AutorizationServer, self).__init__()
        widget = QDialog()
        self.auto_ui = Ui_autorization_server()
        self.auto_ui.setupUi(widget)

        self.auto_ui.btn_enter_malfurik.clicked.connect(self.add_malfurik)
        self.auto_ui.btn_enter_animaunt.clicked.connect(self.add_animaunt)

        malf = Config().get_info_malf()
        if malf[0] != '' and malf[1] != '':
            self.auto_ui.login_malfurik.setText(malf[0])
            self.auto_ui.pass_malfurik.setText(malf[1])
            self.auto_ui.login_malfurik.setDisabled(True)
            self.auto_ui.pass_malfurik.setDisabled(True)
            self.auto_ui.btn_enter_malfurik.setDisabled(True)
            self.auto_ui.btn_enter_malfurik.setText('Авторизован')
        maunt = Config().get_info_maunt()
        if maunt[0] != '' and maunt[1] != '':
            self.auto_ui.animaunt_login.setText(maunt[0])
            self.auto_ui.pass_animaunt.setText(maunt[1])
            self.auto_ui.animaunt_login.setDisabled(True)
            self.auto_ui.pass_animaunt.setDisabled(True)
            self.auto_ui.btn_enter_animaunt.setDisabled(True)
            self.auto_ui.btn_enter_animaunt.setText('Авторизован')

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
                    Config().set_info_malf(login_malf, pass_malf)
            except pysftp.AuthenticationException:
                QMessageBox.warning(None, "Ошибка", "Неверный логин или пароль")
            except Exception as e:
                log_config.setup_logger().exception(e)


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
                    Config().set_info_maunt(login_maunt, pass_maunt)
            except pysftp.AuthenticationException:
                QMessageBox.warning(None, "Ошибка", "Неверный логин или пароль")
            except Exception as e:
                log_config.setup_logger().exception(e)


