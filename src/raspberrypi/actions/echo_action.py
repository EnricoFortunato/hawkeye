from awscrt import mqtt
from actions import Action

class Echo_Action(Action):
    def __init__(self, mqtt_connection):
        super().__init__()
        self.mqtt = mqtt_connection

    def execute(self,topic, payload, dup, qos, retain, **kwargs):
        print(f"Received message from topic '{topic}': {payload}")
        self.mqtt.publish(
            topic="/pi/echo",
            payload=payload,
            qos=mqtt.QoS.AT_LEAST_ONCE)
