from __future__ import absolute_import, unicode_literals
default_app_config = 'myapp.apps.MyAppConfig'



import os
from celery import Celery

# Установите переменную окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moto_store.settings')

# Создайте экземпляр объекта Celery с именем 'celery'
app = Celery('moto_store')

# Загрузите настройки из модуля настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач
app.autodiscover_tasks()

# Определите функцию для получения информации о текущем времени сервера
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
