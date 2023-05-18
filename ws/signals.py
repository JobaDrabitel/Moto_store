from django.db.models.signals import post_save
from django.dispatch import receiver

from myapp.models import User, Product

@receiver(post_save, sender=User)
def user_post_save(sender, instance, **kwargs):
    print("new user!")
    pass

@receiver(post_save, sender=Product)
def product_post_save(sender, instance, **kwargs):
    print("new product!")
    pass
