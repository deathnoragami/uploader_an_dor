import hurdsub_worker.handlers as hardsuber
from PyQt5.QtCore import QThread, pyqtSignal

class WorkerHardSub(QThread):
    def __init__(self, ui, video_path):

        super().__init__()
        self.ui = ui
        self.video_path = video_path

    def run(self):
        path_sub = hardsuber.sub_extract_and_edit(self.video_path)
        hardsuber.video_hardsub(self.video_path, self.ui)