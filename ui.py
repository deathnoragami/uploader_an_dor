# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(804, 474)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(40, 0, 361, 341))
        self.tabWidget.setObjectName("tabWidget")
        self.tabAnime = QtWidgets.QWidget()
        self.tabAnime.setObjectName("tabAnime")
        self.lbl_anime_pic = QtWidgets.QLabel(self.tabAnime)
        self.lbl_anime_pic.setGeometry(QtCore.QRect(10, 50, 331, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lbl_anime_pic.setFont(font)
        self.lbl_anime_pic.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lbl_anime_pic.setScaledContents(False)
        self.lbl_anime_pic.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_anime_pic.setWordWrap(False)
        self.lbl_anime_pic.setObjectName("lbl_anime_pic")
        self.lbl_anime_video = QtWidgets.QLabel(self.tabAnime)
        self.lbl_anime_video.setGeometry(QtCore.QRect(10, 10, 331, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lbl_anime_video.setFont(font)
        self.lbl_anime_video.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_anime_video.setObjectName("lbl_anime_video")
        self.line_nondefoult_number_anime = QtWidgets.QLineEdit(self.tabAnime)
        self.line_nondefoult_number_anime.setGeometry(QtCore.QRect(20, 90, 121, 31))
        self.line_nondefoult_number_anime.setObjectName("line_nondefoult_number_anime")
        self.progress_anime = QtWidgets.QProgressBar(self.tabAnime)
        self.progress_anime.setGeometry(QtCore.QRect(20, 280, 331, 23))
        self.progress_anime.setProperty("value", 24)
        self.progress_anime.setObjectName("progress_anime")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tabAnime)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 120, 160, 151))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.check_sftp_anime = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.check_sftp_anime.setObjectName("check_sftp_anime")
        self.verticalLayout.addWidget(self.check_sftp_anime)
        self.check_mult_anime = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.check_mult_anime.setObjectName("check_mult_anime")
        self.verticalLayout.addWidget(self.check_mult_anime)
        self.check_nonlink_anime = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.check_nonlink_anime.setObjectName("check_nonlink_anime")
        self.verticalLayout.addWidget(self.check_nonlink_anime)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.tabAnime)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(180, 120, 160, 151))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_pic_anime = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btn_pic_anime.setObjectName("btn_pic_anime")
        self.verticalLayout_2.addWidget(self.btn_pic_anime)
        self.btn_video_anime = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btn_video_anime.setObjectName("btn_video_anime")
        self.verticalLayout_2.addWidget(self.btn_video_anime)
        self.btn_upload_anime = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btn_upload_anime.setObjectName("btn_upload_anime")
        self.verticalLayout_2.addWidget(self.btn_upload_anime)
        self.tabWidget.addTab(self.tabAnime, "")
        self.tabDorama = QtWidgets.QWidget()
        self.tabDorama.setObjectName("tabDorama")
        self.pushButton_5 = QtWidgets.QPushButton(self.tabDorama)
        self.pushButton_5.setGeometry(QtCore.QRect(30, 170, 75, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.tabDorama)
        self.pushButton_6.setGeometry(QtCore.QRect(30, 130, 75, 23))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.tabDorama)
        self.pushButton_7.setGeometry(QtCore.QRect(30, 100, 75, 23))
        self.pushButton_7.setObjectName("pushButton_7")
        self.progressBar = QtWidgets.QProgressBar(self.tabDorama)
        self.progressBar.setGeometry(QtCore.QRect(30, 70, 291, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(self.tabDorama)
        self.label.setGeometry(QtCore.QRect(130, 30, 47, 21))
        self.label.setObjectName("label")
        self.checkBox_4 = QtWidgets.QCheckBox(self.tabDorama)
        self.checkBox_4.setGeometry(QtCore.QRect(30, 220, 70, 17))
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_5 = QtWidgets.QCheckBox(self.tabDorama)
        self.checkBox_5.setGeometry(QtCore.QRect(30, 250, 70, 17))
        self.checkBox_5.setObjectName("checkBox_5")
        self.checkBox_6 = QtWidgets.QCheckBox(self.tabDorama)
        self.checkBox_6.setGeometry(QtCore.QRect(30, 280, 70, 17))
        self.checkBox_6.setObjectName("checkBox_6")
        self.tabWidget.addTab(self.tabDorama, "")
        self.text_last_dub = QtWidgets.QTextEdit(self.centralwidget)
        self.text_last_dub.setGeometry(QtCore.QRect(40, 350, 361, 81))
        self.text_last_dub.setObjectName("text_last_dub")
        self.text_send_dub = QtWidgets.QTextEdit(self.centralwidget)
        self.text_send_dub.setGeometry(QtCore.QRect(610, 20, 181, 221))
        self.text_send_dub.setObjectName("text_send_dub")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(410, 20, 191, 411))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 189, 409))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.btn_search_dubs = QtWidgets.QPushButton(self.centralwidget)
        self.btn_search_dubs.setGeometry(QtCore.QRect(614, 402, 171, 31))
        self.btn_search_dubs.setObjectName("btn_search_dubs")
        self.line_id_chat = QtWidgets.QLineEdit(self.centralwidget)
        self.line_id_chat.setGeometry(QtCore.QRect(610, 250, 181, 20))
        self.line_id_chat.setObjectName("line_id_chat")
        self.line_search_dub_name_serial = QtWidgets.QLineEdit(self.centralwidget)
        self.line_search_dub_name_serial.setGeometry(QtCore.QRect(610, 280, 181, 20))
        self.line_search_dub_name_serial.setObjectName("line_search_dub_name_serial")
        self.line_search_dub_number_serial = QtWidgets.QLineEdit(self.centralwidget)
        self.line_search_dub_number_serial.setGeometry(QtCore.QRect(610, 310, 181, 20))
        self.line_search_dub_number_serial.setObjectName("line_search_dub_number_serial")
        self.line_count_dubbers = QtWidgets.QLineEdit(self.centralwidget)
        self.line_count_dubbers.setGeometry(QtCore.QRect(610, 340, 181, 20))
        self.line_count_dubbers.setObjectName("line_count_dubbers")
        self.line_prefix_name_serial = QtWidgets.QLineEdit(self.centralwidget)
        self.line_prefix_name_serial.setGeometry(QtCore.QRect(610, 370, 181, 20))
        self.line_prefix_name_serial.setObjectName("line_prefix_name_serial")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setEnabled(False)
        self.pushButton.setGeometry(QtCore.QRect(-1, 90, 21, 231))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 804, 21))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menuBar)
        self.menu_application = QtWidgets.QAction(MainWindow)
        self.menu_application.setObjectName("menu_application")
        self.menu_vk = QtWidgets.QAction(MainWindow)
        self.menu_vk.setObjectName("menu_vk")
        self.menu_tg = QtWidgets.QAction(MainWindow)
        self.menu_tg.setObjectName("menu_tg")
        self.menu_server = QtWidgets.QAction(MainWindow)
        self.menu_server.setCheckable(True)
        self.menu_server.setObjectName("menu_server")
        self.menu.addAction(self.menu_application)
        self.menu.addAction(self.menu_vk)
        self.menu.addAction(self.menu_tg)
        self.menu.addAction(self.menu_server)
        self.menuBar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Animaunt"))
        self.lbl_anime_pic.setText(_translate("MainWindow", "Картинка не выбрана"))
        self.lbl_anime_video.setText(_translate("MainWindow", "Видео не выбрано"))
        self.line_nondefoult_number_anime.setPlaceholderText(_translate("MainWindow", "Номер серии"))
        self.check_sftp_anime.setText(_translate("MainWindow", "SFTP"))
        self.check_mult_anime.setText(_translate("MainWindow", "Мультфильмы"))
        self.check_nonlink_anime.setText(_translate("MainWindow", "Без ссылок"))
        self.btn_pic_anime.setText(_translate("MainWindow", "Картинка"))
        self.btn_video_anime.setText(_translate("MainWindow", "Видео"))
        self.btn_upload_anime.setText(_translate("MainWindow", "Загрузить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAnime), _translate("MainWindow", "Аниме"))
        self.pushButton_5.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_6.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_7.setText(_translate("MainWindow", "PushButton"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.checkBox_4.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_5.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_6.setText(_translate("MainWindow", "CheckBox"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDorama), _translate("MainWindow", "Дорамы"))
        self.btn_search_dubs.setText(_translate("MainWindow", "Найти"))
        self.line_id_chat.setToolTip(_translate("MainWindow", "Айди нужной беседы в которой дабберы сдают дороги."))
        self.line_id_chat.setPlaceholderText(_translate("MainWindow", "ID chat"))
        self.line_search_dub_name_serial.setToolTip(_translate("MainWindow", "<html><head/><body><p>Название серии, как подписывали дабберы (если папка называется по другому или же просто найти без выбора картинки)</p></body></html>"))
        self.line_search_dub_name_serial.setPlaceholderText(_translate("MainWindow", "Название серии"))
        self.line_search_dub_number_serial.setPlaceholderText(_translate("MainWindow", "№ серии"))
        self.line_count_dubbers.setPlaceholderText(_translate("MainWindow", "Кол-во даб."))
        self.line_prefix_name_serial.setPlaceholderText(_translate("MainWindow", "Префикс sp, фильм и тд."))
        self.pushButton.setText(_translate("MainWindow", "<-"))
        self.menu.setTitle(_translate("MainWindow", "Авторизация"))
        self.menu_application.setText(_translate("MainWindow", "Приложение"))
        self.menu_vk.setText(_translate("MainWindow", "ВКонтакте"))
        self.menu_tg.setText(_translate("MainWindow", "Телеграм"))
        self.menu_server.setText(_translate("MainWindow", "Сервер"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
