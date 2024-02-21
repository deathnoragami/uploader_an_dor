from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui import Ui_MainWindow

from autorization.autorization_application.autorizade_app import AuthorizationApp
from autorization.autorization_vk.autorizade_vk import AuthorizationVK
from autorization.autorization_tg.autorizade_tg import AuthorizationTG
from autorization.autorization_server.autorizade_sftp import AutorizationServer

from autorization.autorization_animaunt.autorization_web_animaunt import Animaunt_web
from autorization.autorization_malfurik.autorization_web_malfurik import Malfurik_web


import sys
import os
from dotenv import load_dotenv

from qt_material import apply_stylesheet

import connect_firebase


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.center_screen()
        db = connect_firebase.Connect()
        
        ########## ПРОВЕРКА АВТОРИЗАЦИИ ##################################
        
        user_autorization = False
        if os.path.isfile('assets/session_timmers'):
            with open('assets/session_timmers', 'r') as file:
                uid = file.read()
                user_data = db.find_user_uid(uid)
                if user_data:
                    self.ui.block_screen.hide()
                    user_autorization = True
                    
        if user_autorization == False:
            self.ui.menu_vk.setDisabled(True)
            self.ui.menu_tg.setDisabled(True)
            self.ui.menu_server.setDisabled(True)
            
        ##################################################################


        ########## Добавление чекбоксов дабберов #############################
        
        dub_data = db.get_dub_data()
        self.ui.scrollAreaWidgetContents.setLayout(QtWidgets.QVBoxLayout())
        sorted_result = sorted(dub_data, key=lambda x: x['id'])
        self.checkbox_vars = []
        for item in sorted_result:
            checkbox = QtWidgets.QCheckBox(item['id'])
            ping_value = item.get('ping', '')
            self.checkbox_vars.append((checkbox, ping_value, item['id']))
            self.ui.scrollAreaWidgetContents.layout().addWidget(checkbox)
                
        #####################################################################
        
        
        ############# МЕНЮ ВЕРНХЕЕ ####################################
        
        self.ui.menu_application.triggered.connect(AuthorizationApp)
        self.ui.menu_vk.triggered.connect(AuthorizationVK)
        self.ui.menu_tg.triggered.connect(AuthorizationTG)
        self.ui.menu_server.triggered.connect(AutorizationServer)
        
        #####################################################################


        self.ui.btn_pic_anime.clicked.connect(Malfurik_web)

        
        db.close()
    def test(self):
        selected_data = []
        for checkbox, ping_value, item_id in self.checkbox_vars:
            if checkbox.isChecked():
                selected_data.append({item_id, ping_value})
        
        print(selected_data)
    
    
    def center_screen(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_dotenv()
    apply_stylesheet(app, theme='dark_cyan.xml')
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
