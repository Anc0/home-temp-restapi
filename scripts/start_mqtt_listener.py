from mqtt.tasks import subscribe_to_mqtt

class MqttSubscribe:

    def __init__(self):
        pass

    @staticmethod
    def run():
        subscribe_to_mqtt.delay()
