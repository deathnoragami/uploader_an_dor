from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
from config import Config as cfg

import os

class PictureSelectorAnime(QObject):
    picture_selected = pyqtSignal(str)

    def select_picture(self):
        path = cfg().get_defoult_path_pic_anime()
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(None, "Выбрать изображение", path, "Images (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if file_path:
            cfg().set_defoult_path_pic_anime(os.path.dirname(os.path.dirname(file_path)))
            self.picture_selected.emit(file_path)