from celery import Celery

# Создание экземпляра Celery
app = Celery('moto_store')

# Загрузка конфигурации Celery из настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач Celery из файлов tasks.py в Django приложениях
app.autodiscover_tasks()
