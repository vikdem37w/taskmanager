import aiogram
import logging
from taskmgr.settings import REMINDERS_CHAT_IDS, TELEGRAM_KEY


async def send_notification(message):
    bot = aiogram.Bot(token=TELEGRAM_KEY)
    logger = logging.getLogger(__name__)
    for chat_id in REMINDERS_CHAT_IDS:
        try:
            await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
            logger.info(f"Reminder to {chat_id} sent successfully")
        except Exception as e:
            logger.error(f"Error sending notification to chat {chat_id}: {e}")
    await bot.session.close()
