from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

# use the ProtocolTypeRouter class provided by Channels as the main entry point of your routing system
# (standard ProtocolTypeRouter router automatically maps HTTP requests to the standard Django views if no specific http mapping is provided.)
application = ProtocolTypeRouter({
# ProtocolTypeRouter takes a dictionary that maps communication types like http or websocket to ASGI applications. You instantiate this class with an empty
# dictionary that later you will fill with a route for your chat application WebSocket consumer.
    'websocket': AuthMiddlewareStack(
# AuthMiddlewareStack class provided by Channels supports standard Django authentication, where the user details are stored in the session. You plan to access the user instance in the scope of the consumer to identify the user who sends a message
# ---------------------------------------------------------------------------------------
# In this code, you use URLRouter to map websocket connections to the URL patterns defined in the websocket_urlpatterns list of the chat application routing file
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
