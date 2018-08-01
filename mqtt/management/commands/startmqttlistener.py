from django.core.management.base import BaseCommand
from mqtt.tasks import subscribe_to_mqtt


class Command(BaseCommand):
    help = 'Starts the mqtt listener'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        subscribe_to_mqtt()
