
# import os
# from django.urls import path
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from forum.consumers import NewsFeedConsumer

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_forum_backend.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": 
#         URLRouter([
#             path("ws/questions/", NewsFeedConsumer.as_asgi()),  # WebSocket URL
#         ])
#     ,
# })


import os
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from forum.consumers import NewsFeedConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "online_forum_backend.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handles HTTP requests
    "websocket": AuthMiddlewareStack(  # Handles WebSocket requests with authentication
        URLRouter([
            path("ws/questions/", NewsFeedConsumer.as_asgi()),  # WebSocket URL
        ])
    ),
})
