import requests
from environs import Env
# import aiogram



env = Env()
env.read_env()
TELEGRAM_KEY = env("TELEGRAM_KEY")
# bot = aiogram.Bot(token=TELEGRAM_KEY)

def send_notification(message, chat_id):
    
    url = f"https://api.telegram.org/bot{TELEGRAM_KEY}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }
    requests.post(url, json=payload)

    # bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")