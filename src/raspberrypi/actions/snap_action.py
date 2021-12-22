from awscrt import mqtt
from actions import Action
import json
import boto3
from botocore.exceptions import ClientError
import os
from datetime import datetime
import logging
log = logging.getLogger(__name__)


class Snap_Action(Action):
    bucket = "hawkeye-data-storage"

    def __init__(self, mqtt_connection):
        super().__init__()
        self.mqtt = mqtt_connection

    def execute(self, topic, payload):
        log.info(f"Received snap request on {topic}")
        msg = json.loads(payload)

        # take a snap

        # load to s3
        url = self.upload_file(self.bucket,"test-image.png")

        msg = {"location" : url}
        self.mqtt.publish(
            topic="pi/snap",
            payload=json.dumps(msg),
            qos=mqtt.QoS.AT_LEAST_ONCE)

    def upload_file(self, BUCKET, data):
        # Upload a file to our S3 bucket
        try:
            s3 = boto3.resource('s3')
            bucket = s3.Bucket(BUCKET)
            filename = 'pi/snip/' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '.json'
            bucket.put_object(Body=data,Key=filename)
            url = f'https://{BUCKET}.s3.amazonaws.com/{filename}'
            log.info(f"Loaded snap request to {url}")

        except Exception as e:
            log.exception("Failed to upload to s3")
            url = 'Failed to capture image'

        except TypeError as e:
            log.error("Failed to upload to s3")
            url = 'Failed to capture image'

        finally:
            return url