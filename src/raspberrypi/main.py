import logging
logging_level = logging.WARNING
logging.basicConfig(filename='/home/pi/Documents/hawkeye/logs/log.log', filemode='a', level=logging_level, format='%(asctime)s - %(levelname)s - %(module)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S')
log = logging.getLogger(__name__)
log.info("Started execution")

import argparse
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import sys
import threading
import time
from uuid import uuid4
import json
import os
from events import Echo_Event, Snap_Event


# coded configurations
message = "I am home"
home_topic = "pi/home"
client_id= "raspberrypi-"+str(uuid4())
counter = 5

# loaded configurations
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'settings.json')

with open(filename) as setting_file:
    args = json.load(setting_file)

io.init_logging(getattr(io.LogLevel, "Warn"), 'stderr')

received_count = 0
received_all_event = threading.Event()


# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))


# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(on_resubscribe_complete)


def on_resubscribe_complete(resubscribe_future):
        resubscribe_results = resubscribe_future.result()
        print("Resubscribe results: {}".format(resubscribe_results))

        for topic, qos in resubscribe_results['topics']:
            if qos is None:
                sys.exit("Server rejected resubscribe to topic: {}".format(topic))


class Event_Handler():

    def __init__(self) -> None:
        self.mqtt_connection = self.establish_mqtt_connection()
        self.events = []

    def establish_mqtt_connection(self):
        event_loop_group = io.EventLoopGroup(1)
        host_resolver = io.DefaultHostResolver(event_loop_group)
        client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

        self.mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=args["end-point"],
            port= 8883,
            cert_filepath=args["cert"],
            pri_key_filepath=args["key"],
            client_bootstrap=client_bootstrap,
            ca_filepath=args["root-ca"],
            on_connection_interrupted=on_connection_interrupted,
            on_connection_resumed=on_connection_resumed,
            client_id=client_id,
            clean_session=False,
            keep_alive_secs=30,
            http_proxy_options=None)

        print(f"Connecting to {args['end-point']} with client ID '{client_id}'...")

        connect_future = self.mqtt_connection.connect()

        # Future.result() waits until a result is available
        connect_future.result()
        print("Connected!")


    def revoke_mqtt_connection(self):
        print("Disconnecting...")
        disconnect_future = self.mqtt_connection.disconnect()
        disconnect_future.result()
        print("Disconnected!")


    def add_event(self,Event,*args,**kwargs):
        # event can be an external trigger(button pressed) or 
        # action can be to publish something 
        self.events.append(Event(*args,**kwargs))



my_handler = Event_Handler()
my_handler.establish_mqtt_connection()
my_handler.add_event(Echo_Event,my_handler.mqtt_connection)
my_handler.add_event(Snap_Event,my_handler.mqtt_connection)

keep_running = True

while keep_running:
    keyboard = input(":")
    if keyboard == "q" or keyboard == "quit" or keyboard=="exit":
        keep_running = False
    else:
        time.sleep(1)

my_handler.revoke_mqtt_connection()




