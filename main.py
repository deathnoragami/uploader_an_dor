'''
from qt_material import apply_stylesheet
apply_stylesheet(app, theme='dark_cyan.xml')


self.scrollAreaWidgetContents.setLayout(QtWidgets.QVBoxLayout())
sorted_result = dict(sorted(dub_data.items()))
self.checkbox_vars = []
for key, value in sorted_result.items():
    checkbox = QtWidgets.QCheckBox(key)
    if isinstance(value, dict):
        ping_value = value.get('ping')
    self.checkbox_vars.append((checkbox, ping_value, key))
    self.scrollAreaWidgetContents.layout().addWidget(checkbox)''' # Рабочее
