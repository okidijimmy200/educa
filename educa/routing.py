from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
# import chat.routing

# use the ProtocolTypeRouter class provided by Channels as the main entry point of your routing system
application = ProtocolTypeRouter({
# ProtocolTypeRouter takes a dictionary that maps communication types like http or websocket to ASGI applications. You instantiate this class with an empty
# dictionary that later you will fill with a route for your chat application WebSocket consumer.
    # 'websocket': AuthMiddlewareStack(
    #     URLRouter(
    #         chat.routing.websocket_urlpatterns
    #     )
    # ),
})
