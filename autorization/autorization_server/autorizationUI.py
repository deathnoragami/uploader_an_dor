# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\autorization\autorization_server\autoUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_autorization_server(object):
    def setupUi(self, autorization_server):
        autorization_server.setObjectName("autorization_server")
        autorization_server.resize(451, 148)
        autorization_server.setMinimumSize(QtCore.QSize(451, 148))
        autorization_server.setMaximumSize(QtCore.QSize(451, 148))
        self.animaunt_login = QtWidgets.QLineEdit(autorization_server)
        self.animaunt_login.setGeometry(QtCore.QRect(10, 30, 131, 31))
        self.animaunt_login.setObjectName("animaunt_login")
        self.pass_animaunt = QtWidgets.QLineEdit(autorization_server)
        self.pass_animaunt.setGeometry(QtCore.QRect(150, 30, 141, 31))
        self.pass_animaunt.setObjectName("pass_animaunt")
        self.login_malfurik = QtWidgets.QLineEdit(autorization_server)
        self.login_malfurik.setGeometry(QtCore.QRect(10, 90, 131, 31))
        self.login_malfurik.setObjectName("login_malfurik")
        self.pass_malfurik = QtWidgets.QLineEdit(autorization_server)
        self.pass_malfurik.setGeometry(QtCore.QRect(150, 90, 141, 31))
        self.pass_malfurik.setObjectName("pass_malfurik")
        self.btn_enter_animaunt = QtWidgets.QPushButton(autorization_server)
        self.btn_enter_animaunt.setGeometry(QtCore.QRect(310, 30, 121, 31))
        self.btn_enter_animaunt.setObjectName("btn_enter_animaunt")
        self.btn_enter_malfurik = QtWidgets.QPushButton(autorization_server)
        self.btn_enter_malfurik.setGeometry(QtCore.QRect(310, 90, 121, 31))
        self.btn_enter_malfurik.setObjectName("btn_enter_malfurik")

        self.retranslateUi(autorization_server)
        QtCore.QMetaObject.connectSlotsByName(autorization_server)

    def retranslateUi(self, autorization_server):
        _translate = QtCore.QCoreApplication.translate
        autorization_server.setWindowTitle(_translate("autorization_server", "Авторизация на сервере"))
        self.animaunt_login.setStatusTip(_translate("autorization_server", "Логин для анимаунта"))
        self.animaunt_login.setPlaceholderText(_translate("autorization_server", "Логин Анимаунт"))
        self.pass_animaunt.setPlaceholderText(_translate("autorization_server", "Пароль Анимаунт"))
        self.login_malfurik.setPlaceholderText(_translate("autorization_server", "Логин малфурик"))
        self.pass_malfurik.setPlaceholderText(_translate("autorization_server", "Пароль малфурик"))
        self.btn_enter_animaunt.setText(_translate("autorization_server", "Войти"))
        self.btn_enter_malfurik.setText(_translate("autorization_server", "Войти"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    autorization_server = QtWidgets.QWidget()
    ui = Ui_autorization_server()
    ui.setupUi(autorization_server)
    autorization_server.show()
    sys.exit(app.exec_())
