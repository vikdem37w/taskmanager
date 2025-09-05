import aiogram
from taskmgr.settings import REMINDERS_CHAT_IDS, TELEGRAM_KEY


async def send_notification(message):
    bot = aiogram.Bot(token=TELEGRAM_KEY)
    for chat_id in REMINDERS_CHAT_IDS:
        await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
    await bot.session.close()
