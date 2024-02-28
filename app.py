from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from ui import Ui_MainWindow

from autorization.autorization_application.autorizade_app import AuthorizationApp
from autorization.autorization_vk.autorizade_vk import AuthorizationVK
from autorization.autorization_tg.autorizade_tg import AuthorizationTG
from autorization.autorization_server.autorizade_sftp import AutorizationServer
from autorization.autorization_animaunt.autorization_web_animaunt import Animaunt_web
from autorization.autorization_malfurik.autorization_web_malfurik import Malfurik_web

from work_files.select_pic_anime import PictureSelectorAnime
from work_files.select_video_anime import VideoSelectorAnime
from work_files.upload_anime import UploadManager
from work_files.database_title import DatabaseManager
from work_files.dubbers import Dubbers

from config import Config

import sys
import os
import glob
from dotenv import load_dotenv

from qt_material import apply_stylesheet

import connect_firebase


load_dotenv()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.center_screen()
        db = connect_firebase.Connect()

        ############## ОБНУЛЕНИЕ ПЕРЕМЕННЫХ #############################
        
        self.file_path_anime_pic = None
        self.file_path_anime_video = None
        self.link_site_animaunt = None
        self.link_malf_anime = None
        
        #################################################################


        ########## ПРОВЕРКА АВТОРИЗАЦИИ ##################################

        user_autorization = False
        config = Config()
        uid = config.get_uid_program()
        if not uid == '':
            user_data = db.find_user_uid(uid)
            if user_data:
                self.ui.block_screen.hide()
                user_autorization = True

        if not user_autorization:
            self.ui.menu_vk.setDisabled(True)
            self.ui.menu_tg.setDisabled(True)
            self.ui.menu_server.setDisabled(True)
            self.ui.menu_animaunt.setDisabled(True)
            self.ui.menu_2.setDisabled(True)

        ##################################################################

        self.ui.btn_search_dubs.clicked.connect(self.btn_search_dub)
    
        ########## Добавление чекбоксов дабберов #############################

        self.dub_data = db.get_dub_data()
        self.ui.scrollAreaWidgetContents.setLayout(QtWidgets.QVBoxLayout())
        sorted_result = sorted(self.dub_data, key=lambda x: x['id'])
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

        self.ui.btn_upload_anime.clicked.connect(self.start_work)
        self.upload_manager = UploadManager(self)
        self.upload_manager.signals.progress_changed.connect(self.update_progress)
        self.upload_manager.signals.upload_signals.connect(self.upload_finished)
        self.upload_manager.signals.post_signal.connect(self.upload_vk_finish)

        self.ui.check_malf_anime.stateChanged.connect(self.toggle_site_anime)
        #######################################################################

        ######################### СДАЧА ДОРОГ #################################

        self.ui.line_id_chat.setText(Config().get_id_chat())
        self.ui.line_id_chat.textChanged.connect(self.save_id_chat)

        #######################################################################

        db.close()

    ################ АНИМЕ КНОПКИ ############################################ 
 
    def start_work(self):
        try:
            if self.file_path_anime_pic is not None:
                   
                if self.ui.check_post_site.isChecked():
                    if not self.ui.link_site.text().startswith(os.getenv('CHECK_ANIMAUNT_LINK')) or self.ui.link_site.text() == '':
                        QMessageBox.warning(None, "Ошибка", "Ссылка указана не верно")
                        return
                    else:
                        self.link_site_animaunt = self.ui.link_site.text()
                if self.ui.check_malf_anime.isChecked():
                    if not self.ui.link_malfurik_anime.text().startswith(os.getenv('CHECK_MALFURIK_LINK')) or self.ui.link_malfurik_anime.text() == '':
                        QMessageBox.warning(None, "Ошибка", "Ссылка указана не верно")
                        return
                    else:
                        self.link_malf_anime = self.ui.link_malfurik_anime.text()
                        
                self.upload_manager.start_upload(self.file_path_anime_pic,
                                                self.file_path_anime_video,
                                                self.ui.check_sftp_anime.isChecked(),
                                                self.ui.check_malf_anime.isChecked(),
                                                self.ui.check_nonlink_anime.isChecked(),
                                                self.ui.check_post_site.isChecked(),
                                                self.link_site_animaunt,
                                                self.link_malf_anime,
                                                self.check_data, )
            else:
                QMessageBox.warning(None, "Ошибка", "Картинка не выбрана!")
        except Exception as e:
            self.file_path_anime_pic = None
            self.file_path_anime_video = None
            QMessageBox.warning(None, "Ошибка", f"Ошибка: {e}")
            
    def update_progress(self, value, mb_upload, mb_total, speed):
        self.ui.progress_anime.setValue(value)
        self.ui.progress_value.setText(f'Загружено: {mb_upload:.1f} МБ из {mb_total:.1f} МБ. Скорость: {speed:.1f} МБ/с')

    def upload_finished(self, result):
        name_folder = os.path.basename(os.path.dirname(self.file_path_anime_pic))
        self.ui.logging_upload.append(name_folder + " загружен в " + result)

    def upload_vk_finish(self, end):
        self.file_path_anime_pic = None 
        self.file_path_anime_video = None
        self.ui.btn_upload_anime.setDisabled(True)
        self.ui.check_malf_anime.setChecked(False)
        self.ui.check_nonlink_anime.setChecked(False)
        self.ui.check_post_site.setChecked(False)
        self.ui.check_sftp_anime.setChecked(False)
        self.ui.lbl_anime_pic.setText("Картинка не выбрана")
        self.ui.btn_video_anime.setText("Выбрать видео")
        if end:
            self.ui.logging_upload.append("Запощено в вк!")
            self.ui.logging_upload.append("____________________________________\n\n")
        else:
            self.ui.logging_upload.append("Отмена загрузки.")
            self.ui.logging_upload.append("____________________________________\n\n")

        


    def select_picture_anime(self):
        self.picture_selector_anime.select_picture()

    def update_label_pic_anime(self, file_path):
        file_name_without_extension, extension = os.path.splitext(os.path.basename(file_path))
        folder_name = os.path.basename(os.path.dirname(file_path))
        self.ui.lbl_anime_pic.setText(f"{folder_name} серия {file_name_without_extension}")
        self.file_path_anime_pic = file_path
        dbm = DatabaseManager()
        self.data = dbm.search_by_path_pic_anime(os.path.dirname(self.file_path_anime_pic))
        if not self.data:
            self.check_data = False
        else:
            self.check_data = True
            if self.data[0]["path_video"] == None or self.data[0]["path_video"] == "":
                self.file_path_anime_video = None
            else:
                search_number = str(file_name_without_extension.zfill(2))
                search_pattern = os.path.join(self.data[0]["path_video"], f"{search_number}*.mp4")
                try:
                    video_file = glob.glob(search_pattern)[0]
                    self.update_label_video_anime(video_file)
                except:
                    video_file = None
                

            self.ui.check_sftp_anime.setChecked(self.data[0]["check_sftp"])
            self.ui.check_nonlink_anime.setChecked(self.data[0]["check_nolink"])
            self.ui.check_malf_anime.setChecked(self.data[0]["check_malf"])
            self.ui.check_post_site.setChecked(self.data[0]["check_post_site"])
            self.ui.link_site.setText(self.data[0]["link_site"])
        self.ui.btn_upload_anime.setDisabled(False)
        Dubbers().find_send_vk(path=file_path, main_window_ui=self)
        

    def select_video_anime(self):
        self.video_selector_anime.select_video()

    def update_label_video_anime(self, file_path):
        if file_path == "":
            self.file_path_anime_video = None
            self.ui.btn_video_anime.setText("Выбрать видео")
        else:
            file_name = os.path.basename(file_path)
            file_name_without_extension, extension = os.path.splitext(os.path.basename(file_path))
            folder_name = os.path.basename(os.path.dirname(file_path))
            self.ui.btn_video_anime.setText(f"Серия {file_name}")
            self.file_path_anime_video = file_path

    def toggle_site_anime(self, state):
        if state == Qt.Checked:
            self.ui.link_malfurik_anime.setEnabled(True)
        else:
            self.ui.link_malfurik_anime.setEnabled(False)

    ##########################################################################

    ###########################  СДАЧА ДОРОГ #################################

    def save_id_chat(self, id):
        Config().set_id_chat(id)
        
    def btn_search_dub(self):
        Dubbers().find_send_vk(btn=True, main_window_ui=self)

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
    apply_stylesheet(app, theme='dark_cyan.xml')
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
