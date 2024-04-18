from telegram import Bot
import asyncio
import os

async def send_ad(name_ad, serial_number, serial_name, login):
    bot = Bot(token=os.getenv("TG_API_BOT"))
    await bot.send_message(chat_id=os.getenv("TG_ID_CHAT_AD"), 
                           text=f"<b>Название:</b>\n{serial_name} серия {serial_number}\n\n<b>Реклама</b>\n<blockquote>{name_ad}</blockquote>\n\nДелал <b>{login}</b>", 
                           parse_mode='HTML')

async def send_message(login, serial_number, serial_name):
    bot = Bot(token=os.getenv("TG_API_BOT"))
    await bot.send_message(chat_id=os.getenv("TG_ID_CHAT"), 
                           text=f"<b>{login}</b> загрузил дораму <b>{serial_name} серия {serial_number}</b>", 
                           parse_mode='HTML')
    
async def find_message(target_text):
    bot = Bot(token="7129615885:AAHGyxyobYmCGHY5LjK5L9in2-nQu0qHEkI")

def main(msg_type, *args):
    if msg_type == "logger":
        asyncio.run(send_message(*args))
    if msg_type == "ad":
        asyncio.run(send_ad(*args))

    
