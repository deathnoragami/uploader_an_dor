from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
import os

class VideoSelectorAnime(QObject):
    video_selected = pyqtSignal(str)

    def select_video(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(None, "Выбрать видео", "", "Video (*.mp4)", options=options)
        if file_path:
            self.video_selected.emit(file_path)
        else:
            self.video_selected.emit(None)