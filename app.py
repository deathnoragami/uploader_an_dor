from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
    
from ui import Ui_MainWindow
from autorizade_app import AuthorizationWindow

import sys
import os

from qt_material import apply_stylesheet

import connect_firebase


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.center_screen()


        ########## Добавление чекбоксов дабберов #############################
        db = connect_firebase.Connect()
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
        db.close()
        
        #####################################################################
        
        if os.path.exists('assets/session_timmers'):
            self.ui.menu_application.setDisabled(True)
        
        ############# МЕНЮ ВЕРНХЕЕ ####################################
        self.ui.menu_application.triggered.connect(AuthorizationWindow)
        
        print(self.checkbox_vars)
        #####################################################################

    
    
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
