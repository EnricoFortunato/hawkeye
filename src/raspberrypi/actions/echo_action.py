from awscrt import mqtt
from actions import Action
import json
import logging
log = logging.getLogger(__name__)

class Echo_Action(Action):
    def __init__(self, mqtt_connection):
        super().__init__()
        self.mqtt = mqtt_connection

    def execute(self, topic, payload, dup, qos, retain, **kwargs):
        msg = json.loads(payload)
        log.info(f"Received message on {topic}: {msg}")
        log.info(f"Republishing same message ...")
        self.mqtt.publish(
            topic="pi/echo",
            payload=payload,
            qos=mqtt.QoS.AT_LEAST_ONCE)
        log.info(f"Done")
