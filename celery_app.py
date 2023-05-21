import os
from celery import Celery
from datetime import datetime, time

# Установка переменной окружения с настройками Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moto_store.settings')

# Создание экземпляра Celery
app = Celery('moto_store')

# Загрузка настроек из файла настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач в файлах tasks.py внутри ваших приложений
app.autodiscover_tasks()
