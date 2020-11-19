import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone

# ChatConsumer consumer. This class inherits from the Channels websocketConsumer class to implement a basic WebSocket consumer
class ChatConsumer(AsyncWebsocketConsumer):
# connnect(): Called when a new connection is received. You accept any connection with self.accept(). You can also reject a connection by calling self.close().
    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = 'chat_%s' % self.id
        # join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # accept connection
        await self.accept()
# disconnect(): Called when the socket closes. You use pass because you don't need to implement any action when a client closes the connection
    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
# receive(): Called whenever data is received. You expect text to be received as text_data (this could also be binary_data for binary data). You treat the text data received as JSON. Therefore, you use json.loads() to load the received JSON data into a Python dictionary. You access the message
# key, which you expect to be present in the JSON structure received. To echo the message, you send the message back to the WebSocket with self. send(), transforming it in JSON format again through json.dumps().
    # receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()

        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )

    # receive message from room group
    async def chat_message(self, event):
        # send message to WebSocket
        await self.send(text_data=json.dumps(event))
