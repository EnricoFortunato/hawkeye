from events import Event
from actions import Snap_Action
from awscrt import mqtt

class Snap(Event):
    def __init__(self, mqtt_connection):
        super().__init__()

        print(f"Subscribing to topic /pi/snap/request")
        subscribe_future, packet_id = mqtt_connection.subscribe(
            topic="/pi/snap/request",
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=Snap_Action(mqtt_connection).execute
            )

        subscribe_result = subscribe_future.result()
        print(f"Subscribed with {str(subscribe_result['qos'])}")

