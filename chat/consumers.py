import json
from pyexpat.errors import messages

from channels.generic.websocket import AsyncWebsocketConsumer
from kafka import KafkaConsumer
from django.conf import settings
from twisted.names.root import bootstrap
import asyncio

from watchfiles import awatch


class KafkaWebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.consumer_task = asyncio.create_task(self.consume_message_from_kafka())


    async def disconnect(self, close_code):
        # if hasattr(self,close_code):
        if hasattr(self,"consumer_task"):
            self.consumer_task.cancel()





    async def receive(self, text_data):
        message = json.loads(text_data)
        await self.send(text_data=json.dumps({
            'message':message['message']
            }))

    async def consume_message_from_kafka(self):
        loop = asyncio.get_event_loop()

        def create_consumer():
            return KafkaConsumer(
                'message_topic',
                    bootstrap_servers=settings.KAFKA_CONSUMER_CONFIG['bootstrap_servers'],
                    group_id=settings.KAFKA_CONSUMER_CONFIG['group_id'],
                    value_deserializer=settings.KAFKA_CONSUMER_CONFIG['value_deserializer'],
            )
        consumer = await loop.run_in_executor(None,create_consumer)
        while True:
            msg = await loop.run_in_executor(None,consumer.poll,1,0)
            if msg:
                for _, records in msg.items():
                    for record in records:
                        await self.send_to_websocket(record.value)

    async def send_to_websocket(self,message):
        self.send(text_data=json.dumps({
            'message':message
        }))