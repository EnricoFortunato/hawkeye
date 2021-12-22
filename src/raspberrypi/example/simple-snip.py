import logging
import boto3
from botocore.exceptions import ClientError
import os
from datetime import datetime

# settings
bucket = "hawkeye-data-storage"

# log
levels = {
    'Debug': logging.DEBUG,
    'Info': logging.INFO,
    'Warning': logging.WARNING,
    'Error': logging.ERROR
}

LOGGING_LEVEL = 'Debug'
logging.basicConfig(filename='/home/pi/Documents/hawkeye/logs/log.log', filemode='a', level=levels[LOGGING_LEVEL], format='%(asctime)s - %(levelname)s - %(module)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S')
log = logging.getLogger(__name__)
log.info("Started execution")


def upload_file(BUCKET, data):
    # Upload a file to our S3 bucket
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(BUCKET)
        filename = '/pi/snip/' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '.json'
        bucket.put_object(Body=data,Key=filename)
        url = f'https://{BUCKET}.s3.amazonaws.com/{filename}'

    except Exception as e:
        log.exception("Failed to upload to s3")
        url = 'Failed to capture image'

    finally:
        return url

url = upload_file(bucket,"test-image.png")
print(url)