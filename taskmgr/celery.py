from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from environs import Env
# import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmgr.settings')

from django.conf import settings
# django.setup()

settings.configure()

result_backend = 'django-db'

env = Env()
env.read_env()

app = Celery('taskmgr', broker=f'pyamqp://{env.str("MQ_USER")}:{env.str("MQ_PASSWORD")}@localhost/vhost')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(related_name="tg_notifier")

@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    from tasks.tg_notifier import send_deadline_notifications
    sender.add_periodic_task(10.0, send_deadline_notifications.s(), name="send_deadline_notifications")