# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from mqtt.helpers import MqttClient


@shared_task
def subscribe_to_mqtt():
    client = MqttClient()
    client.run()