from environs import Env
import requests
from celery import shared_task
from datetime import datetime
from django.utils.timezone import make_aware
from .models import Task, UserProfile
from celery import Celery
from celery.schedules import crontab

env = Env()
env.read_env()

TELEGRAM_KEY = env("TELEGRAM_KEY")



app = Celery()

@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        10.0, # crontab(hour=9, minute=0),
        send_deadline_notifications.s(),
    )



def send_telegram_notification(chat_id, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_KEY}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }
    response = requests.post(url, json=payload)
    return response.json()



@shared_task
def send_deadline_notifications():
    now = make_aware(datetime.now().strftime("%Y-%m-%d"))
    upcoming_deadline = now 

    tasks_due_soon = Task.objects.filter(due_date__lte=upcoming_deadline)

    for task in tasks_due_soon:
        user = task.user
        chat_id = 1096766653 #TEST, I'LL BE BURNED AT A STAKE IF I PUSH THIS TO GIT

        if chat_id:
            telegram_message = f"*{user.username}*, isn't there something you've forgotten to do? \n*{task.title}* is waiting."
            send_telegram_notification(chat_id, telegram_message)