from datetime import datetime
import logging
import asyncio
from celery import shared_task
from django.utils.timezone import make_aware
from .tg_notifier import send_notification
from .models import Task


@shared_task
def send_deadline_notifications():
    now = make_aware(datetime.now())
    today = now.date()

    logger = logging.getLogger(__name__)

    tasks_due_soon = Task.objects.filter(due_date__lte=today)
    logger.info(f"Found {tasks_due_soon.count()} tasks due soon")

    for task in tasks_due_soon:
        try:
            asyncio.run(
                send_notification(
                    f"*{task.user.username}*, aren't you forgetting something important? \n*{task.title}* is waiting."
                )
            )
        except RuntimeError as e:
            logger.error(f"Reminder failed: {e}")
