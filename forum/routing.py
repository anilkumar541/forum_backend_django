from django.urls import path
from .consumers import NewsFeedConsumer

websocket_urlpatterns = [
    path('ws/questions/', NewsFeedConsumer.as_asgi()),
]