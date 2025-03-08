from kafka import KafkaConsumer
from django.conf import settings
import json

from sqlparse.engine.grouping import group

consumer  = KafkaConsumer(
    'message_topic',
            bootstrap_servers=settings.KAFKA_CONSUMER_CONFIG['bootstrap.servers'],
            group_id=settings.KAFKA_CONSUMER_CONFIG['group_id'],
            value_deserializer=settings.KAFKA_CONSUMER_CONFIG['value_deserializer'],
)

def consume_message_from_kafka():
    print("Kafka consumer ishga tushdi...")
    for message in consumer:
        process_message(message.value)

def process_message(message):
    print(f"Receiver message: {message}")
