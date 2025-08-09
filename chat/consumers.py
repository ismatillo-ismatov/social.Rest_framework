from channels.db import database_sync_to_async
from django.utils.dateparse import parse_datetime
import json
import asyncio

from redis import asyncio as aioredis
from channels.generic.websocket import AsyncWebsocketConsumer
from decouple import config
import httpx

UPSTASH_REDIS_REST_URL = config("UPSTASH_REDIS_REST_URL")
UPSTASH_REDIS_REST_TOKEN = config("UPSTASH_REDIS_REST_TOKEN")



@database_sync_to_async
def get_profile_by_user(user):
    from user_profile.models import UserProfile
    return UserProfile.objects.select_related("userName").get(userName=user)

@database_sync_to_async
def get_profile_by_id(profile_id):
    from user_profile.models import UserProfile
    return UserProfile.objects.select_related("userName").get(id=profile_id)







@database_sync_to_async
def save_message(sender_profile,receiver_profile,message_text,type_='text',file=None,replied_to=None):
    from .models import Message
    return Message.objects.create(
        sender=sender_profile,
        receiver=receiver_profile,
        message=message_text,
        type=type_,
        file=file,
        replied_to_id=replied_to,
    )

@database_sync_to_async
def mark_single_as_read(sender_profile_id,receiver_profile_id,timestamp_iso):
    from .models import Message
    dt = parse_datetime(timestamp_iso)
    Message.objects.filter(
        sender_id=sender_profile_id,
        receiver_id=receiver_profile_id,
        timestamp=dt,
    ).update(is_read=True)


class RedisConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        self.room_name = f"{self.sender_id}_{self.receiver_id}"
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        messages = await self.get_messages()
        for msg in messages:
            await self.send(text_data=json.dumps({
                'message': msg
            }))

    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        sender_id = data.get('sender')
        receiver_id = data.get('receiver')
        if not message or not sender_id or not receiver_id:
            await self.send(text_data=json.dumps({'error': 'message, sender va receiver monydolari kerak'}))
            return

        try:
            sender = await get_profile_by_id(sender_id)
            receiver = await get_profile_by_id(receiver_id)
            msg = await save_message(
                sender_profile=sender,
                receiver_profile=receiver,
                message_text=message,
                type_=data.get('type','text'),
                file=data.get('file'),
                replied_to=data.get('replied_to'),
            )
            payload = {
                'id':msg.id,
                'sender_id': sender.id,
                'receiver_id': receiver.id,
                'sender_name': sender.userName.username,
                'receiver_name': receiver.userName.username,
                'message': msg.message,
                'type': msg.type,
                'file': msg.file.url if msg.file else None,
                'is_read': msg.is_read,
                'timestamp': msg.timestamp.isoformat(),
                'replied_to': msg.replied_to_id,
                'replied_to_text': msg.replied_to.message if msg.replied_to else None,
                'replied_to_sender_id': msg.replied_to.sender.id if msg.replied_to else None,
                'replied_to_sender_name': msg.replied_to.sender.userName.username if msg.replied_to else None,
                'replied_to_ts': msg.replied_to.timestamp.isoformat() if msg.replied_to else None,
            }

            await self.channel_layer.group_send(
                f"chat_{self.sender_id}_{self.receiver_id}",
                {'type':'chat_message','message':payload}
            )
            await self.channel_layer.group_send(
                f"chat_{self.receiver_id}_{self.sender_id}",
                {'type': 'chat_message','message': payload}
            )

        except Exception as e:
            await self.send(text_data=json.dumps({'error': f'Xabar saqlashda xato: {str(e)}'}))
    async def chat_message(self,event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message':message
        }))



    async def get_messages(self,count=10):
        async with httpx.AsyncClient() as client:
            redis_key = f"room:{self.room_name}:messages"
            redis_url = f"{UPSTASH_REDIS_REST_URL}/lrange/{redis_key}/0/{count - 1}"
            headers = {"Authorization": f"Bearer {UPSTASH_REDIS_REST_TOKEN}"}
            response = await client.get(redis_url,headers=headers)

            if response.status_code == 200:
                data = response.json()
                return data.get("result",[])
            return []




