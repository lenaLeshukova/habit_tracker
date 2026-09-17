import os
from celery import Celery

# Устанавливаем дефолтный модуль настроек Django для celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Используем строку конфигурации из settings.py с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим задачи (tasks.py) во всех зарегистрированных приложениях
app.autodiscover_tasks()
