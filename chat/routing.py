from django.urls import re_path #re_path to define the path with regular expressions.
from . import consumers

websocket_urlpatterns = [
    # map a URL pattern with the ChatConsumer class that you defined in the chat/consumers.py file
    re_path(r'ws/chat/room/(?P<course_id>\d+)/$', consumers.ChatConsumer),
]
'''URL includes an integer parameter called course_id.
This parameter will be available in the scope of the consumer and will allow you
to identify the course chat room that the user is connecting to.'''

# NB:
'''It is a good practice to prepend WebSocket URLs with /ws/ to
differentiate them from URLs used for standard synchronous HTTP
requests. This also simplifies the production setup when an HTTP
server routes requests based on the path'''