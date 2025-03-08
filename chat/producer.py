from kafka import  KafkaProducer
import json
from django.conf import settings

try:
    producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_PRODUCER_CONFIG['bootstrap_servers'],
    value_serializer=settings.KAFKA_PRODUCER_CONFIG['value_serializer'],
)
    print("Kafka producer movfaqiyatli yaratildi")
except Exception as e:
    print(f"Kafka producer yaratishda xatolik: ${e}")

try:
    def send_message_to_kafka(topic,message):
        producer.send(topic,message)
        print(f'Kafka yuborildi: {message}')
        producer.flush()
except Exception as e:
    print(f'Yuborildi: {e}')