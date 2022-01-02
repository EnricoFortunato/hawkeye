import json
import boto3

client = boto3.client('iot-data', region_name='eu-west-1')



def lambda_handler(event, context):
    print(event)
    # TODO implement
    # Change topic, qos and payload
    response = client.publish(
        topic='pi/snap/request',
        qos=1,
        payload=json.dumps({"requester":"snap request API"})
    )
    print(response)
    
    return {
        'statusCode': 200,
        'body': json.dumps({"result":"success"})
    }
