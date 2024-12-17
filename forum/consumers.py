# your_app_name/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NewsFeedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'newsfeed_room'  # A room for newsfeed updates
        self.room_group_name = f"questions_feed"

        # Join the newsfeed group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the newsfeed group
        await self.channel_layer.group_discard(
            "questions_feed",
            self.channel_name
        )

    # Receive message from WebSocket
    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #     print(text_data, message, ">>>>>>>>>>>>>>>>>>>>")

    #     # Send the message to the group
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'newsfeed_message',
    #             'message': message
    #         }
    #     )

    # Receive message from group
    async def send_new_question(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
