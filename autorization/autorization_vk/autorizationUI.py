# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\autorization_vk\autoUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_authorization_vk(object):
    def setupUi(self, authorization_vk):
        authorization_vk.setObjectName("authorization_vk")
        authorization_vk.setEnabled(True)
        authorization_vk.resize(412, 110)
        authorization_vk.setMinimumSize(QtCore.QSize(412, 110))
        authorization_vk.setMaximumSize(QtCore.QSize(412, 110))
        authorization_vk.setFocusPolicy(QtCore.Qt.TabFocus)
        authorization_vk.setWindowOpacity(1.0)
        self.line_token_vk = QtWidgets.QLineEdit(authorization_vk)
        self.line_token_vk.setGeometry(QtCore.QRect(30, 20, 351, 31))
        self.line_token_vk.setObjectName("line_token_vk")
        self.btn_autho_vk = QtWidgets.QPushButton(authorization_vk)
        self.btn_autho_vk.setGeometry(QtCore.QRect(240, 60, 141, 31))
        self.btn_autho_vk.setObjectName("btn_autho_vk")

        self.retranslateUi(authorization_vk)
        QtCore.QMetaObject.connectSlotsByName(authorization_vk)

    def retranslateUi(self, authorization_vk):
        _translate = QtCore.QCoreApplication.translate
        authorization_vk.setWindowTitle(_translate("authorization_vk", "Авторизация в ВКонтакте"))
        self.line_token_vk.setToolTip(_translate("authorization_vk", "<html><head/><body><p><span style=\" font-size:10pt;\">Заходим на сайт </span><span style=\" font-size:10pt; font-weight:600; text-decoration: underline;\">https://vkhost.github.io</span><span style=\" font-size:10pt;\">,нажимаем &quot;Настройки&quot;, выбираем пункты [Сообщения, Доступ в любое время, Группы] и получить. Авторизуемся через свой аккаунт, копируем ссылку открывшего окна и вставляем сюда.</span></p></body></html>"))
        self.line_token_vk.setPlaceholderText(_translate("authorization_vk", "Токен ВКонтакте"))
        self.btn_autho_vk.setText(_translate("authorization_vk", "Войти"))
