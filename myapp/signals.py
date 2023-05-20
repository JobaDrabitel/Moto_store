from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from myapp.models import User

channel_layer = get_channel_layer()

@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        print('user')
        async_to_sync(channel_layer.group_send)("notifications", {
            "type": "notify_new_user",
            "text": "New user registered"
        })
