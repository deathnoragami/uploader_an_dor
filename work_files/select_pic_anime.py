from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
import os

class PictureSelectorAnime(QObject):
    picture_selected = pyqtSignal(str)

    def select_picture(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(None, "Выбрать изображение", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if file_path:
            self.picture_selected.emit(file_path)