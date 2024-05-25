# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Python\Uploader\autorization\autorization_server\autoUI.ui'
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
        autorization_server.setStyleSheet("QWidget{\n"
"    background-color:rgb(49, 54, 65) ;\n"
"}\n"
"QToolTip {\n"
"        color: black; /* Цвет текста */\n"
"        background-color: white; /* Цвет фона */\n"
"        border: 1px solid black; /* Граница */\n"
"        font: 12px; /* Шрифт */\n"
"}\n"
"QFrame{\n"
"    background-color: rgb(49, 54, 65);\n"
"    border:none;\n"
"    border-radius:0px;\n"
"}\n"
"/* Стиль кнопок */\n"
"QPushButton {\n"
"    background-color: rgb(38, 42, 51);\n"
"    color: rgb(52, 181, 249); /* текст в кнопках светлее голубой */\n"
"    border: none;\n"
"    border-radius:15px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(44, 50, 60);\n"
"    color: rgb(52, 181, 249); /* текст в кнопках светлее голубой */\n"
"    border: 1px solid rgb(0, 72, 127);\n"
"}\n"
"QPushButton::disabled {\n"
"    color: rgba(52, 181, 249,50%);\n"
"    background-color: rgba(38, 42, 51,50%);\n"
"}\n"
"\n"
"/* Стиль прогрессбара */\n"
"QProgressBar {\n"
"    background-color: rgb(38, 42, 51);\n"
"    color: rgb(49, 54, 65);\n"
"    border-radius: 10px;\n"
"}\n"
"QProgressBar::chunk {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.511364, x2:1, y2:0.523, stop:0 rgba(52, 181, 249, 255), stop:1 rgba(0, 116, 211, 255));\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"\n"
"/* Стиль чекбоксов */\n"
"QCheckBox {\n"
"    color: rgb(140, 151, 170); /* светлосерый текст */\n"
"    border: none;\n"
"    spacing:10px;\n"
"    font-size:15px;\n"
"}\n"
"QCheckBox::indicator{\n"
"    width:15px;\n"
"    height:15px;\n"
"}\n"
"QCheckBox::indicator:unchecked{\n"
"    image: url(:/ckeckbox/icon/checkbox_unchecked.ico);\n"
"}\n"
"QCheckBox::indicator:unchecked:hover, QCheckBox::indicator:unchecked:pressed {\n"
"    image: url(:/ckeckbox/icon/checkbox_unchecked_hover_pressed.ico);\n"
"}\n"
"QCheckBox::indicator:checked{\n"
"    image: url(:/ckeckbox/icon/checkbox_checked.ico);\n"
"}\n"
"QCheckBox::indicator:checked:hover, QCheckBox::indicator:checked:pressed {\n"
"image: url(:/ckeckbox/icon/checkbox_checked_hover_pressed.ico);\n"
"}\n"
"QCheckBox:hover {\n"
"    color:rgb(52, 181, 249);\n"
"}\n"
"QCheckBox::disabled{\n"
"    color: rgba(140, 151, 170,30%);\n"
"}\n"
"\n"
"/* Стиль текстового поля */\n"
"QTextEdit, QLineEdit {\n"
"    background-color: rgb(38, 42, 51);\n"
"    color: rgb(140, 151, 170); /* светлосерый текст */\n"
"    border: none;\n"
"    border-radius: 15px;\n"
"}\n"
"\n"
"/* Стиль стакедвиджета */\n"
"QStackedWidget {\n"
"    background-color: rgb(38, 42, 51);\n"
"    border: none;\n"
"    border-radius: 15px;\n"
"    padding: 0px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: rgb(140, 151, 170);\n"
"}\n"
"\n"
"\n"
"QScrollBar:vertical {\n"
"        background: rgb(38, 42, 51);\n"
"        width: 12px;\n"
"        margin: 0px 0px 0px 0px;\n"
"    }\n"
"QScrollBar::handle:vertical {\n"
"        background: rgb(49, 54, 65);\n"
"        min-height: 20px;\n"
"    }\n"
"QScrollBar::handle:vertical:hover {\n"
"        background: rgb(52, 181, 249);\n"
"    }\n"
"    QScrollBar::add-line:vertical {\n"
"        background: rgb(38, 42, 51);\n"
"        height: 0px;\n"
"        subcontrol-position: bottom;\n"
"        subcontrol-origin: margin;\n"
"    }\n"
"    QScrollBar::sub-line:vertical {\n"
"        background: rgb(38, 42, 51);\n"
"        height: 0px;\n"
"        subcontrol-position: top;\n"
"        subcontrol-origin: margin;\n"
"    }\n"
"    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"        background: none;\n"
"    }\n"
"\n"
"rgb(38, 42, 51) темно серый\n"
"rgb(49, 54, 65) тоже темно серый, чутка светлее\n"
"rgb(140, 151, 170) светлосерый текст\n"
"\n"
"rgb(0, 116, 211) голубой\n"
"rgb(42, 150, 255) светлоголубой\n"
"rgb(52, 181, 249) еще  светлее голубой")
        self.animaunt_login = QtWidgets.QLineEdit(autorization_server)
        self.animaunt_login.setGeometry(QtCore.QRect(10, 30, 131, 31))
        self.animaunt_login.setObjectName("animaunt_login")
        self.pass_animaunt = QtWidgets.QLineEdit(autorization_server)
        self.pass_animaunt.setGeometry(QtCore.QRect(150, 30, 141, 31))
        self.pass_animaunt.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_animaunt.setObjectName("pass_animaunt")
        self.login_malfurik = QtWidgets.QLineEdit(autorization_server)
        self.login_malfurik.setGeometry(QtCore.QRect(10, 90, 131, 31))
        self.login_malfurik.setObjectName("login_malfurik")
        self.pass_malfurik = QtWidgets.QLineEdit(autorization_server)
        self.pass_malfurik.setGeometry(QtCore.QRect(150, 90, 141, 31))
        self.pass_malfurik.setEchoMode(QtWidgets.QLineEdit.Password)
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
