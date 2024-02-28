from PyQt5.QtWidgets import QMessageBox

class CustomMessageBox:
    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.show()

    def show(self):
        reply = QMessageBox()
        reply.setWindowTitle(self.title)
        reply.setText(self.text)
        reply.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply.button(QMessageBox.Yes).setText("Да")
        reply.button(QMessageBox.No).setText("Нет")
        result = reply.exec_()
        if result == QMessageBox.Yes:
            return True
        else:
            return False