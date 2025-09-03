from environs import Env
import requests
from celery import shared_task
from datetime import datetime
from django.utils.timezone import make_aware
from .models import Task
import logging
import os
from django.conf import settings
settings.configure()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmgr.settings')

env = Env()
env.read_env()

TELEGRAM_KEY = env("TELEGRAM_KEY")
REMINDERS_CHAT_IDS = env("REMINDER_CHAT_IDS", []).split(",")


@shared_task
def send_deadline_notifications():
    now = make_aware(datetime.now().strftime("%Y-%m-%d"))
    upcoming_deadline = now 

    tasks_due_soon = Task.objects.filter(due_date__lte=upcoming_deadline)
    logging.info("Attempting to send a reminder")
    logging.info(f"Tasks due soon: {tasks_due_soon}")
    for task in tasks_due_soon:
        user = task.user

        for chat_id in REMINDERS_CHAT_IDS:
            telegram_message = f"*{user.username}*, isn't there something you've forgotten to do? \n*{task.title}* is waiting."
            url = f"https://api.telegram.org/bot{TELEGRAM_KEY}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": telegram_message,
                "parse_mode": "Markdown",
            }
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                logging.info(f"Reminder about {task.title} sent to {user.username} successfully")
            else:
                logging.error(f"Failed to send reminder about {task.title} to {user.username}")
                logging.error(response.json())