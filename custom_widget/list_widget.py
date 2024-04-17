from PyQt5.QtGui import QDragEnterEvent, QDragMoveEvent
from PyQt5.QtWidgets import QAbstractItemView, QListWidget, QListWidgetItem, QWidget
from PyQt5.QtCore import Qt, QUrl


class ListboxWidget(QListWidget):
    def __init__(self, parent: None) -> None:
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(381, 435)
        
