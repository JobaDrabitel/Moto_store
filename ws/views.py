from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()

# Отправка уведомления о новом пользователе в группу "notifications"
async_to_sync(channel_layer.group_send)("notifications", {"type": "notify_new_user", "text": "New user registered"})
