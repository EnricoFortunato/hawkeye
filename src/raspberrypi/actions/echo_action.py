from awscrt import mqtt
from actions import Action
import json

class Echo_Action(Action):
    def __init__(self, mqtt_connection):
        super().__init__()
        self.mqtt = mqtt_connection

    def execute(self,topic, payload, dup, qos, retain, **kwargs):
        msg = json.loads(payload)
        print(f"Received message on {topic}: {msg}")
        print(f"Republishing same message ...")
        self.mqtt.publish(
            topic="/pi/echo",
            payload=payload,
            qos=mqtt.QoS.AT_LEAST_ONCE)
        print(f"Done")
