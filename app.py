from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui import Ui_MainWindow

from autorization.autorization_application.autorizade_app import AuthorizationApp
from autorization.autorization_vk.autorizade_vk import AuthorizationVK
from autorization.autorization_tg.autorizade_tg import AuthorizationTG
from autorization.autorization_server.autorizade_sftp import AutorizationServer
from autorization.autorization_animaunt.autorization_web_animaunt import Animaunt_web
from autorization.autorization_malfurik.autorization_web_malfurik import Malfurik_web

from work_files.select_pic_anime import PictureSelectorAnime
from work_files.select_video_anime import VideoSelectorAnime
from work_files.upload_anime import upload_anime


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
            self.ui.menu_animaunt.setDisabled(True)
            self.ui.menu_2.setDisabled(True)
            
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
        
        self.ui.menu_animaunt.triggered.connect(Animaunt_web)
        self.ui.menu_malfurik.triggered.connect(Malfurik_web)
        
        #####################################################################

        ############### Аниме выбор, кнопки ###################################

        self.picture_selector_anime = PictureSelectorAnime()
        self.picture_selector_anime.picture_selected.connect(self.update_label_pic_anime)
        self.ui.btn_pic_anime.clicked.connect(self.select_picture_anime)
        
        self.video_selector_anime = VideoSelectorAnime()
        self.video_selector_anime.video_selected.connect(self.update_label_video_anime)
        self.ui.btn_video_anime.clicked.connect(self.select_video_anime)
        
        self.ui.btn_upload_anime.clicked.connect(self.upload_anime)
        
        
        #######################################################################
        
        db.close()
        
    ################ АНИМЕ КНОПКИ ############################################ 
       
    def select_picture_anime(self):
        self.picture_selector_anime.select_picture()
        
    def update_label_pic_anime(self, file_path):
        file_name_without_extension, extension = os.path.splitext(os.path.basename(file_path))
        folder_name = os.path.basename(os.path.dirname(file_path))
        self.ui.lbl_anime_pic.setText(f"{folder_name} серия {file_name_without_extension}")
        self.file_path_anime_pic = file_path
        
    def select_video_anime(self):
        self.video_selector_anime.select_video()
        
    def update_label_video_anime(self, file_path):
        if file_path == "":
            self.file_path_anime_video = None
            self.ui.lbl_anime_video.setText(f"Видео не выбрано")
        else:
            file_name_without_extension, extension = os.path.splitext(os.path.basename(file_path))
            folder_name = os.path.basename(os.path.dirname(file_path))
            self.ui.lbl_anime_video.setText(f"{folder_name} серия {file_name_without_extension}")
            self.file_path_anime_video = file_path
        
    def upload_anime(self):
        if hasattr(self, 'file_path_anime_pic') and self.file_path_anime_pic:
            if not hasattr(self, 'file_path_anime_video'):
                self.file_path_anime_video = None
            upload_anime(self.file_path_anime_pic, 
                         self.file_path_anime_video,
                         self.ui.check_sftp_anime.isChecked(),
                         self.ui.check_mult_anime.isChecked(),
                         self.ui.check_nonlink_anime.isChecked())
        else:
            QMessageBox.warning(None, "Ошибка", "Каритнка не выбрана!")
        
    ##########################################################################

        
        
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
