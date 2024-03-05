from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
from config import Config as cfg

import os

class VideoSelectorDorama(QObject):
    video_selected = pyqtSignal(str)

    def select_video(self):
        path = cfg().get_defoult_path_video_dorama()
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(None, "Выбрать видео", path, "Video (*.mp4)", options=options)
        if file_path:
            cfg().set_defoult_path_video_dorama(os.path.dirname(os.path.dirname(file_path)))
            self.video_selected.emit(file_path)
        else:
            self.video_selected.emit(None)