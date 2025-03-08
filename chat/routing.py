from django.urls import path, re_path
from .consumers import KafkaWebSocketConsumer
websocket_urlpatterns = [
    # path("ws/chat/<int:sender>/<int:receiver>/",ChatConsumer.as_asgi()),
    re_path(r'ws/messages/$',KafkaWebSocketConsumer.as_asgi()),
    # path(r'ws/messages/',KafkaWebSocketConsumer.as_asgi()),
]