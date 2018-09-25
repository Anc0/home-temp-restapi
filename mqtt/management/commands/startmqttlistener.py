from django.core.management.base import BaseCommand

from mqtt.helpers import MqttClient


class Command(BaseCommand):
    help = 'Starts the mqtt listener'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        MqttClient().run()
