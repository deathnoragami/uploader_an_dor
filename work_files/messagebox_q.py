from PyQt5.QtWidgets import QMessageBox

class CustomMessageBox:
    def __init__(self, title, text):
        self.title = title
        self.text = text

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

# from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QListWidget, QPushButton

# class CustomMessageBox(QDialog):
#     def __init__(self, items):
#         super().__init__()
#         self.selected_item = None

#         layout = QVBoxLayout()

#         self.list_widget = QListWidget()
#         self.list_widget.addItems(items)
#         layout.addWidget(self.list_widget)

#         self.ok_button = QPushButton("OK")
#         self.ok_button.clicked.connect(self.handle_ok)
#         layout.addWidget(self.ok_button)

#         self.setLayout(layout)

#     def handle_ok(self):
#         selected_items = self.list_widget.selectedItems()
#         if selected_items:
#             self.selected_item = selected_items[0].text()
#             self.accept()

# def show_custom_message_box(items):
#     app = QApplication([])
#     dialog = CustomMessageBox(items)
#     if dialog.exec_() == QDialog.Accepted:
#         return dialog.selected_item
#     else:
#         return None

# Пример использования
# if __name__ == "__main__":
#     app = QApplication([])
#     items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
#     selected_item = show_custom_message_box(items)
#     if selected_item is not None:
#         print("Выбранный элемент:", selected_item)
#     else:
#         print("Выбор отменен")