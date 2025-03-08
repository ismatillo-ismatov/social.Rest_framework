from django.core.management.base import BaseCommand
from .consumer import consume_message_from_kafka


class Command(BaseCommand):
    help = 'Consume kafka messages and save them to database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("✅ Kafka consumer ishga tushdi..."))
        consume_message_from_kafka()