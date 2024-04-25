from telegram import Bot
import asyncio
import os
from pyrogram import Client

import resource_path


async def send_ad(name_ad, serial_number, serial_name, login):
    text = f"<b>Название:</b>\n<b>{serial_name}</b> серия <b>{serial_number}</b>\n\n<u>Реклама</u>\n<b>{name_ad}</b>\n\nДелал <b>{login}</b>"
    app = Client(resource_path.path("logger_tg"))
    await app.start()
    await app.send_message(chat_id=os.getenv("TG_ID_CHAT_AD"),
                           text=text)
    await app.stop()


async def send_message(login, serial_number, serial_name):
    text = f"<b>{login}</b> загрузил <b>{serial_name} серия {serial_number}</b>"
    app = Client(resource_path.path("logger_tg"))
    await app.start()
    await app.send_message(chat_id=os.getenv("TG_ID_CHAT"),
                           text=text)
    await app.stop()


async def find_message(target_text):
    from pyrogram import Client
    client = Client("assets/my_session_tg")
    await client.start()
    async for message in client.search_messages(os.getenv("TG_ID_CHAT_AD"), limit=1, query=target_text):
        print(message.text)
        pass
    await client.stop()
    return message.text


def main(msg_type, *args):
    if msg_type == "logger":
        asyncio.run(send_message(*args))
    if msg_type == "ad":
        asyncio.run(send_ad(*args))
    if msg_type == "find":
        return asyncio.run(find_message(*args))

#
# if __name__ == "__main__":
#     # text()
#     main("find", "молодая")
