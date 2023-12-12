'''
from qt_material import apply_stylesheet
apply_stylesheet(app, theme='dark_cyan.xml')


self.scrollAreaWidgetContents.setLayout(QtWidgets.QVBoxLayout())
sorted_result = dict(sorted(dub_data.items()))
self.checkbox_vars = []
for key, value in sorted_result.items():
    checkbox = QtWidgets.QCheckBox(key)
    if isinstance(value, dict):
        ping_value = value.get('ping')
    self.checkbox_vars.append((checkbox, ping_value, key))
    self.scrollAreaWidgetContents.layout().addWidget(checkbox)''' # Рабочее


import typing
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog
    
from ui import Ui_MainWindow
from autorizationUI import AutorizationUI

import sys

from qt_material import apply_stylesheet

from connect_firebase import Connect


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.center_screen()
        self.ui.btn_pic_anime.clicked.connect(self.btn)
        
        ########### Добавление чекбоксов дабберов #############################
        dub_data = db.get_dub_data()
        self.ui.scrollAreaWidgetContents.setLayout(QtWidgets.QVBoxLayout())
        sorted_result = dict(sorted(dub_data.items()))
        self.checkbox_vars = []
        for key, value in sorted_result.items():
            checkbox = QtWidgets.QCheckBox(key)
            if isinstance(value, dict):
                ping_value = value.get('ping')
            self.checkbox_vars.append((checkbox, ping_value, key))
            self.ui.scrollAreaWidgetContents.layout().addWidget(checkbox)
            
        #######################################################################


    def btn(self):
        print('Кнопка нажата')
        
    
    def center_screen(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":

    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_cyan.xml')
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())