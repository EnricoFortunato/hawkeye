from awscrt import mqtt
from actions import Action
import json
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
import subprocess
import time
import logging
log = logging.getLogger(__name__)


class Snap_Action(Action):
    bucket = "hawkeye-data-storage"
    temp_pic = "/home/pi/Documents/hawkeye/src/raspberrypi/actions/temp.jpg"

    def __init__(self, mqtt_connection):
        super().__init__()
        self.mqtt = mqtt_connection

    def execute(self, topic, payload):
        log.info(f"Received snap request on {topic}")

        # take a snap
        result = self.take_snap()
        print(result)
        msg = {"snap result": result}

        # load to s3 if success
        if result == "success":
            url, upload_result = self.upload_file(self.bucket,self.temp_pic)
            msg["location"] = url
            if upload_result == "success":
                self.clean_snap()
                pass

        # publish result
        self.mqtt.publish(
            topic="pi/snap",
            payload=json.dumps(msg),
            qos=mqtt.QoS.AT_LEAST_ONCE)

    def upload_file(self, BUCKET, file):
        # Upload a file to our S3 bucket
        try:
            s3 = boto3.resource('s3')
            bucket = s3.Bucket(BUCKET)
            key = 'pi/snap/' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '.png'
            bucket.upload_file(file,key)
            url = f'https://{BUCKET}.s3.amazonaws.com/{key}'
            result = "success"
            log.info(f"Loaded snap request to {url}")

        except Exception as e:
            log.exception("Failed to upload to s3")
            url = ""
            result = "failed"

        finally:
            return url, result

    def take_snap(self):
        try:
            cmd = ["libcamera-still  --immediate -t 100 -q 80 -o" + self.temp_pic]
            subprocess.run(cmd, shell=True)
            picture_result = "success"
        except Exception as e:
            print(e)
            picture_result = "failed"
        finally:
            return picture_result
    
    def clean_snap(self):
        # remove the temp picture after uploading
        cmd = ["rm " + self.temp_pic]
        subprocess.run(cmd, shell=True)
