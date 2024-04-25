from pyrogram import Client, errors
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
import os
import re
import time
import asyncio
import socket
import tgcrypto
import log_config


class TgSignals(QObject):
    progress_changed = pyqtSignal(int, float, float, float)


class UploadDoramaTg(QObject):
    def __init__(self):
        super().__init__()
        self.signals = TgSignals()
        self.api_id = int(os.getenv("API_ID"))
        self.api_hash = os.getenv("API_HASH")
        self.chat_id = int(os.getenv("ID_TG_DORAMA"))
        self.start_time = None

    def seach_id_post(self, file_path):
        asyncio.set_event_loop(asyncio.new_event_loop())
        client = Client("assets/my_session_tg", self.api_id, self.api_hash)
        client.start()
        name = os.path.basename(os.path.dirname(file_path))
        messages = client.search_messages(self.chat_id, limit=5, query=name)
        for message in messages:
            if message.caption:
                first_line = message.caption.split("\n")[0]
                client.stop()
                return message.id, first_line
        QMessageBox.information(None, "[TG] Информация", "[TG] Не нашел постов")
        client.stop()
        return None

    def upload_tg(self, file_path, msg_id):
        try:
            asyncio.set_event_loop(asyncio.new_event_loop())
            client = Client("assets/my_session_tg", self.api_id, self.api_hash)
            client.start()
            filename = os.path.splitext(os.path.basename(file_path))[0].replace("x", "").lstrip('0')
            message = client.get_messages(self.chat_id, msg_id).caption
            text_lines = message.split("\n")
            match = re.search(r'\b\d+\b(?!\D*\d)', text_lines[0])
            if match:
                new_first_line = re.sub(r'\b\d+\b(?!\D*\d)', str(filename), text_lines[0])
                text_lines[0] = new_first_line
                new_text = "\n".join(text_lines)
            sock = socket.socket()
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 250 * 1024 * 1024)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 250 * 1024 * 1024)
            client.send_video(chat_id=self.chat_id, video=file_path, width=1920, height=1080, caption=new_text,
                              progress=self.progress)
            client.stop()
            return True
        except Exception as e:
            log_config.setup_logger().exception(e)
            return False

    def progress(self, current, total):
        if self.start_time is None:
            self.start_time = time.time()
        elapsed_time = time.time() - self.start_time
        mb_transferred = current / (1024 * 1024)
        if elapsed_time == 0:
            elapsed_time = 0.1
        speed = mb_transferred / elapsed_time
        mb_total = total / (1024 * 1024)
        percent = current / total * 100
        self.signals.progress_changed.emit(int(percent), float(mb_transferred), float(mb_total), float(speed))
