from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
import os

class UploadVK(QObject):
    vk_signal = pyqtSignal(str, str)
