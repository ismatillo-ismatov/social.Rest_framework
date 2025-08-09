from django.urls import re_path
from chat.consumers import RedisConsumer

websocket_urlpatterns = [
re_path(r'ws/messages/(?P<sender_id>\d+)/(?P<receiver_id>\d+)/', RedisConsumer.as_asgi()),
#     re_path(r'ws/messages/(?P<room_name>\w+)/', RedisConsumer.as_asgi()),
    # re_path(r'ws/messages/',RedisConsumer.as_asgi()),
]