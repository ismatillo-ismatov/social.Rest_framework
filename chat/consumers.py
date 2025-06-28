import json
from datetime import datetime
from pyexpat.errors import messages

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from twisted.conch.ssh.connection import value
import json
import asyncio
from redis import asyncio as aioredis
from channels.generic.websocket import AsyncWebsocketConsumer



REDIS_CHANNEL = 'chat_channel'

@database_sync_to_async
def get_user_profile(user):
    from user_profile.models import UserProfile
    try:
        return UserProfile.objects.select_related("userName").get(userName=user)
    except UserProfile.DoesNotExist:
        return None

@database_sync_to_async
def get_username(profile):
    return profile.userName.username

@database_sync_to_async
def get_profile_by_id(profile_id):
    from user_profile.models import UserProfile

    try:
        return UserProfile.objects.get(id=profile_id)
    except UserProfile.DoesNotExist:
        return None


@database_sync_to_async
def save_message(sender,receiver,message_text):
    from .models import Message

    return Message.objects.create(
        sender=sender,
        receiver=receiver,
        message=message_text,
    )

@database_sync_to_async
def update_message_is_read(sender_username,receiver_id,timestamp):
    from .models import Message
    from django.utils.dateparse import parse_datetime
    from user_profile.models import UserProfile

    try:
        receiver_profile = UserProfile.objects.get(user__id=receiver_id)
        message_time = parse_datetime(timestamp)

        Message.objects.filter(
            sender__userName__username=sender_username,
            receiver=receiver_profile,
            timestamp=message_time
        ).update(is_read=True)

    except Exception as e:
        print("Error updating message is_read:",str(e))

class RedisConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        if not user.is_authenticated:
            await self.close()
            return

        self.user_id = user.id
        self.channel_name = f"chat_channel_{self.user_id}"
        await self.accept()
        self.redis = await aioredis.Redis(host='localhost', port=6379, db=0)
        self.pubsub = self.redis.pubsub()
        await self.pubsub.subscribe(f"chat_channel_{self.user_id}")
        # await self.pubsub.subscribe(REDIS_CHANNEL)
        asyncio.create_task(self.listen_to_redis())

        await self.send(text_data=json.dumps({
            'message': 'Connected to your personal channel!'
        }))


    async def disconnect(self, close_code):
        await self.pubsub.unsubscribe(self.channel_name)
        # await self.pubsub.unsubscribe(REDIS_CHANNEL)
        await self.pubsub.close()
        await self.redis.close()

    async def receive(self, text_data):
        from user_profile.models import UserProfile

        data = json.loads(text_data)

        user = self.scope['user']
        if not user.is_authenticated:
            await self.send(text_data=json.dumps({'error':'Authentication required'}))
            return

        receiver_id = data.get('receiver')
        message_text = data.get('message')
        try:
            receiver_id = int(receiver_id)
        except (TypeError, ValueError):
            await self.send(text_data=json.dumps({'error': 'Receiver ID must be an integer'}))
            return
        if not receiver_id or not message_text:
            await self.send(text_data=json.dumps({'error':'receiver and message are required'}))
            return

        try:
            sender_profile = await get_user_profile(user)
            receiver_profile = await get_profile_by_id(receiver_id)
            if not sender_profile or not receiver_profile:
                await self.send(text_data=json.dumps({'error':'UserProfile not found'}))
                return


            message_obj = await save_message(sender_profile,receiver_profile,message_text)
            sender_username = await get_username(sender_profile)
            receiver_username = await get_username(receiver_profile)

            message_data = {
                "sender": sender_username,
                "receiver": receiver_username,
                "message": message_text,
                "timestamp": message_obj.timestamp.isoformat(),
                "is_read": message_obj.is_read
            }

            await self.redis.publish(f"chat_channel_{receiver_profile.userName.id}",json.dumps(message_data))

        except UserProfile.DoesNotExist:
            await self.send(text_data=json.dumps({'error':'UserProfile not found'}))
    async def listen_to_redis(self):
        async for message in self.pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                if data.get('receiver') == self.scope['user'].id:
                    await update_message_is_read(
                        sender_username=data['sender'],
                        receiver_id=self.scope['user'].id,
                        timestamp=data['timestamp']
                    )
                await self.send(text_data=json.dumps({
                    'from_redis':data
                }))


    # async def listen_to_redis(self):
    #     async for message in self.pubsub.listen():
    #         if message['type'] == 'message':
    #             data = json.loads(message['data'])
    #             await self.send(text_data=json.dumps({
    #                 'from_redis':data
    #             }))
    #
