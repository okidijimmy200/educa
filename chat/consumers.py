import json
from channels.generic.websocket import AsyncWebsocketConsumer
# async_to_sync() helper function to wrap calls to asynchronous channel layer methods
from asgiref.sync import async_to_sync
from django.utils import timezone

# ChatConsumer consumer. This class inherits from the Channels websocketConsumer class to implement a basic WebSocket consumer
class ChatConsumer(AsyncWebsocketConsumer):
# connnect(): Called when a new connection is received. You accept any connection with self.accept(). You can also reject a connection by calling self.close().
    async def connect(self):
# You retrieve the course id from the scope to know the course that the chat room is associated with. You access self.scope['url_route'] ['kwargs ']['course_id'] to retrieve the course_id parameter from
# the URL. Every consumer has a scope with information about its connection, arguments passed by the URL, and the authenticated user, if any
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
# You build the group name with the id of the course that the group corresponds to. Remember that you will have a channel group for each
# course chat room. You store the group name in the room_group_name attribute of the consumer
        self.room_group_name = 'chat_%s' % self.id
        # join room group
# You join the group by adding the current channel to the group. You obtain the channel name from the channel_name attribute of the consumer. You
# use the group_add method of the channel layer to add the channel to the group. You use the async_to_sync() wrapper to use the channel layer asynchronous method
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
# You keep the self.accept() call to accept the WebSocket connection
        # accept connection
        await self.accept()
# disconnect(): Called when the socket closes. You use pass because you don't need to implement any action when a client closes the connection
# connection is closed, you call the group_discard() method of the channel layer to leave the group. You use the async_to_sync() wrapper to use the channel layer asynchronous method.
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
# type: The event type. This is a special key that corresponds to the name of the method that should be invoked on consumers that receive the event. You
# can implement a method in the consumer named the same as the message type so that it gets executed every time a message with that specific type is received.
                'type': 'chat_message',
                # message: The actual message you are sending
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )
# name this method chat_message() to match the type key that is sent to the channel group when a message is received from the WebSocket
    # receive message from room group
    async def chat_message(self, event):
# When a message with type chat_message is sent to the group, all consumers subscribed to the group will receive the message and will execute the chat_message() method. In the chat_ message() method, you send the event message received to the WebSocket
        # send message to WebSocket
        await self.send(text_data=json.dumps(event))
