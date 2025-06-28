from django.urls import re_path
from chat.consumers import RedisConsumer

websocket_urlpatterns = [
    re_path(r'ws/messages/$',RedisConsumer.as_asgi()),
]