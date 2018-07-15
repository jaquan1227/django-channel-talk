from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from . import consumers
from channels.security.websocket import OriginValidator
from .auth_token import TokenAuthMiddleware

application = ProtocolTypeRouter({
    "websocket": OriginValidator(
        TokenAuthMiddleware(
            URLRouter([
                url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
            ])
        ),["*"]
    ),
})

# application = ProtocolTypeRouter({
#     "websocket": OriginValidator(
#         AuthMiddlewareStack(
#             URLRouter([
#                 url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
#             ])
#         ),["*"]
#     ),
# })