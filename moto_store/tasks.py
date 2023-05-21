import pdb
from decimal import Decimal

from celery.schedules import crontab
from django.conf import settings
from celery import Celery
from myapp.models import Product
import pdb

app = Celery('moto_store')
app.config_from_object(settings, namespace='CELERY')

@app.task
def decrease_prices():
    products = Product.objects.all()
    print(products)
    for product in products:
        product.price *= Decimal('0.95')
        print(product.price)
        product.save()

@app.task
def revert_prices():
    products = Product.objects.all()
    for product in products:
        product.price /= Decimal('0.95')
        product.save()


