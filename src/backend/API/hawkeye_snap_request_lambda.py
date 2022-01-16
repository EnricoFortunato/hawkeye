import json
import boto3


BUCKET = "hawkeye-data-storage"

def lambda_handler(msg, context):
    
    if msg["snap result"] == "success":
        url = msg["location"]
        # Add here the s3 action to update the img
        dest_key = "frontend/refresh-image/refresh_image.png"
        print(s3url_to_key(url))
        res = copy_file(s3url_to_key(url),dest_key)
        if res:
            return {
            'statusCode': 200,
            'body': msg["location"]}
        else:
            return {
            'statusCode': 400,
            'body': "Not successful img update from lambda "}
            
        
    else:
        
        # Add here the s3 action to update the img with the error img
        return {
            'statusCode': 400,
            'body': "Not successful img upload from pi"}
        
def copy_file(src_key, dest_key):
    # Upload a file to our S3 bucket
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(BUCKET)
        bucket.copy({"Bucket":BUCKET,"Key":src_key}, dest_key)
        result = True

    except Exception as e:
        print(e)
        result = False

    finally:
        return result

def s3url_to_key(url):
    return url[46:]
