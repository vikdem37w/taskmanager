from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmgr.settings')

app = Celery('taskmgr')

result_backend = 'django-db'

app.config_from_object('django.conf:settings', namespace='CELERY')