import logging

import paho.mqtt.client as mqtt

from api.models import Topic, TopicRecord

logger = logging.getLogger('mqtt-client')


class MqttClient:

    def __init__(self, client_id='restapi', host_ip='localhost', host_port=1883, keepalive=60, topic='temperature/#', qos=0, persistent=True):
        self.client_id = client_id
        self.host_ip = host_ip
        self.host_port = host_port
        self.keepalive = keepalive
        self.topic = topic
        self.qos=qos
        self.persistent = not persistent

    @staticmethod
    def on_connect(mqttc, obj, flags, rc):
        logger.info("rc: " + str(rc))

    @staticmethod
    def on_message(mqttc, obj, msg):
        logger.info("Message received")
        topic_name = str(msg._topic).split("'")[1]
        try:
            topic = Topic.objects.get(name=topic_name)
        except:
            topic = Topic.objects.create(name=topic_name)
        logger.info(topic)
        topic_record = TopicRecord(value=float(str(msg.payload).split("'")[1]), topic=topic)
        topic_record.save()
        topic.set_last_record(topic_record)

    @staticmethod
    def on_subscribe(mqttc, obj, mid, granted_qos):
        logger.info("Subscribed: " + str(mid) + " " + str(granted_qos))

    @staticmethod
    def on_log(mqttc, obj, level, string):
        logger.info(string)

    def run(self):
        # If you want to use a specific client id, use
        # but note that the client id must be unique on the broker. Leaving the client
        # id parameter empty will generate a random id for you.
        mqttc = mqtt.Client(self.client_id, clean_session=self.persistent)

        mqttc.on_message = self.on_message
        mqttc.on_connect = self.on_connect
        mqttc.on_subscribe = self.on_subscribe
        # Uncomment to enable debug messages
        # mqttc.on_log = on_log

        mqttc.connect(self.host_ip, self.host_port, self.keepalive)
        mqttc.subscribe(self.topic, self.qos)

        mqttc.loop_forever()