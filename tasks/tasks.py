from environs import Env
from .tg_notifier import send_notification
from celery import shared_task
from datetime import datetime
from django.utils.timezone import make_aware
from .models import Task
import asyncio

env = Env()
env.read_env()

REMINDERS_CHAT_IDS = env("REMINDER_CHAT_IDS", []).split(",")

@shared_task
def send_deadline_notifications():
    now = make_aware(datetime.now())
    upcoming_deadline = now 

    tasks_due_soon = Task.objects.filter(due_date__lte=upcoming_deadline)
    for chat_id in REMINDERS_CHAT_IDS:  
        for task in tasks_due_soon:
            asyncio.run(send_notification(f"*{task.user.username}*, isn't there something you've forgotten to do? \n*{task.title}* is waiting.", chat_id))
            
