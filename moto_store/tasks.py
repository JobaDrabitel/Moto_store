from celery.schedules import crontab
from django.conf import settings
from celery import Celery
from myapp.models import Product

app = Celery('moto_store')
app.config_from_object(settings, namespace='CELERY')

@app.task
def decrease_prices():
    products = Product.objects.all()
    for product in products:
        product.price = 95  # Уменьшаем цену на 5%
        product.save()

@app.task
def revert_prices():
    products = Product.objects.all()
    for product in products:
        product.price = 99  # Возвращаем цену обратно
        product.save()


