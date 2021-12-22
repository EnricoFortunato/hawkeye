from events import Event
from actions import Echo_Action
from awscrt import mqtt

class Echo(Event):
    def __init__(self, mqtt_connection):
        super().__init__()

        print(f"Subscribing to topic /pi/echo/request")
        subscribe_future, packet_id = mqtt_connection.subscribe(
            topic="/pi/echo/request",
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=Echo_Action(mqtt_connection).execute
            )

        subscribe_result = subscribe_future.result()
        print(f"Subscribed with {str(subscribe_result['qos'])}")

