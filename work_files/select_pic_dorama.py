from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
from config import Config as cfg

import os

class PictureSelectorDorama(QObject):
    picture_selected = pyqtSignal(str)

    def select_picture(self):
        path = cfg().get_defoult_path_pic_dorama()
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(None, "Выбрать изображение", path, "Images (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if file_path:
            cfg().set_defoult_path_pic_dorama(os.path.dirname(os.path.dirname(file_path)))
            self.picture_selected.emit(file_path)
        else:
            self.picture_selected.emit("")