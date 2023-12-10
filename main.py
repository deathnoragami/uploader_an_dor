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


from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from ui import Ui_MainWindow

import sys

from qt_material import apply_stylesheet

from connect_firebase import dub_data

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_pic_anime.clicked.connect(self.btn)
        
        
        ########### Добавление чекбоксов дабберов #############################
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    apply_stylesheet(app, theme='dark_cyan.xml')
    window.show()
    
    sys.exit(app.exec_())