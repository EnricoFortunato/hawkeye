from awscrt import mqtt
from actions import Action
import json

class Snap_Action(Action):
    def __init__(self, mqtt_connection):
        super().__init__()
        self.mqtt = mqtt_connection

    def execute(self,topic, payload, dup, qos, retain, **kwargs):
        print(f"Received snap request on {topic}")

        # take a snap

        # load to s3
        url = "still a test"

        msg = {"location" : url}
        self.mqtt.publish(
            topic="/pi/snap",
            payload=json.dumps(msg),
            qos=mqtt.QoS.AT_LEAST_ONCE)
