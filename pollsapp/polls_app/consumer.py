import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from django.db.models import Q

from .models import Messages

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send_chat_history()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text   = data["message"]
        sender_email   = data["senderEmail"]
        receiver_email = data["receiverEmail"]
        timestamp      = data.get("timestamp", timezone.now().isoformat())

        await self.create_message(sender_email, receiver_email, message_text)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message_text,
                "senderEmail": sender_email,
                "receiverEmail": receiver_email,
                "timestamp": timestamp,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "senderEmail": event["senderEmail"],
            "receiverEmail": event["receiverEmail"],
            "timestamp": event["timestamp"],
        }))

    @database_sync_to_async
    def create_message(self, sender_email, receiver_email, message_text):
        Messages.objects.create(
            senderemail=sender_email,
            receiveremail=receiver_email,
            message=message_text
        )

    @database_sync_to_async
    def get_history(self, email_a, email_b):
        return Messages.objects.filter(
            Q(senderemail=email_a, receiveremail=email_b) |
            Q(senderemail=email_b, receiveremail=email_a)
        ).order_by("time")

    @database_sync_to_async
    def mark_messages_read(self, receiver_email, sender_email):
        Messages.objects.filter(
            senderemail=sender_email,
            receiveremail=receiver_email,
            read=False
        ).update(read=True)

    async def send_chat_history(self):
        parts = self.room_name.split("__")
        def revert_clean(cleaned):
            return cleaned.replace("_at_", "@").replace("_", ".")

        email_a = revert_clean(parts[0])
        email_b = revert_clean(parts[1])

        await self.mark_messages_read(email_a, email_b)
        past_messages = await self.get_history(email_a, email_b)
        for msg in past_messages:
            await self.send(text_data=json.dumps({
                "message": msg.message,
                "senderEmail": msg.senderemail,
                "receiverEmail": msg.receiveremail,
                "timestamp": msg.time.isoformat(),
            }))
