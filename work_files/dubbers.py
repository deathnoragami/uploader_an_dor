import vk_api
import datetime
from config import Config
import os
import re


class Dubbers:
    def __init__(self):
        pass

        # self.dub.select_dubs.connect(self.print_selected_checkboxes)

    def select_checkboxes(self, main_window_ui):
        self.selected_data = []
        checkbox_vars = main_window_ui.checkbox_vars
        for checkbox, ping_value, item_id in checkbox_vars:
            
            if checkbox.isChecked():
                self.selected_data.append(ping_value)
        result_string = ', '.join(self.selected_data)
        self.clear_checkbox(main_window_ui)
        return result_string
    
    def find_send_vk(self, path=None, btn=None, main_window_ui=None):
        self.clear_checkbox(main_window_ui)
        found_message = []
        chat_id = Config().get_id_chat()
        token = Config().get_vk_token()
        if not token:
            return
        vk_session = vk_api.VkApi(token=f'{token}')
        vk = vk_session.get_api()
        def found_msg(message):
            message_datatime = datetime.datetime.fromtimestamp(message['date'])
            current_datetime = datetime.datetime.now()
            time_difference = current_datetime - message_datatime
            if time_difference.days <= 60:
                sender_id = message['from_id']
                links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                   text)
                for link in links:
                    for item in main_window_ui.dub_data:
                        if item.get('link') == sender_id:
                            title = item.get('id')
                            found_message.append(
                                f"{title} {message_datatime.strftime('%d.%m.%Y %H:%M')}")
                            break
                if 'attachments' in message and len(message['attachments']) > 0:
                    for item in main_window_ui.dub_data:
                        if isinstance(item, dict):
                            key = item.get('id')
                            ping_value = item.get('link')
                        else:
                            ping_value = key
                        if sender_id == ping_value:
                            title = key
                            if f"{title} {message_datatime.strftime('%d.%m.%Y %H:%M')}" not in found_message:
                                found_message.append(f"{title} {message_datatime.strftime('%d.%m.%Y %H:%M')}")
                            for checkbox, ping, name in main_window_ui.checkbox_vars:
                                if name == key:
                                    checkbox.setChecked(True)
        if btn:
            number = main_window_ui.ui.line_search_dub_number_serial.text()
            name = main_window_ui.ui.line_search_dub_name_serial.text()
            prefix = main_window_ui.ui.line_prefix_name_serial.text()
        else:
            number = os.path.splitext(os.path.basename(path))[0].replace('x', '').lstrip('0')
            name = os.path.basename(os.path.dirname(path))
            prefix = ''
        result_chat = vk.messages.search(q=f'{name}', peer_id=2000000000+int(chat_id), count=100)
        for message in result_chat['items']:
            if 'text' in message:
                text = message['text'].lower()
                if prefix != '':
                    if f'{prefix}{number}' in text:
                        found_msg(message)
                else:
                    if f'e{number} ' in text or f'е{number} ' in text or f'e {number} ' in text or f'е {number} ' in text or f'e {number}' in text or f'e{number}' in text or f'е {number}' in text or f'е{number}' in text:
                        found_msg(message)
        main_window_ui.ui.text_send_dub.setText("\n".join(list(reversed(found_message))))
        main_window_ui.ui.line_count_dubbers.setText(str(len(found_message)))

    def clear_checkbox(self, main_ui):
        checkbox_vars = main_ui.checkbox_vars
        for checkbox, ping_value, item_id in checkbox_vars:
            if checkbox.isChecked():
                checkbox.setChecked(False)