from datetime import datetime
import asyncio
from celery import shared_task
from django.utils.timezone import make_aware
from .tg_notifier import send_notification
from .models import Task


@shared_task
def send_deadline_notifications():
    now = make_aware(datetime.now())
    upcoming_deadline = now

    tasks_due_soon = Task.objects.filter(due_date__lte=upcoming_deadline)
    for task in tasks_due_soon:
        asyncio.run(
            send_notification(
                f"*{task.user.username}*, aren't you forgetting something important? \n*{task.title}* is waiting."
            )
        )
