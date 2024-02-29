import boto3 
import os
import json


s3 = boto3.client('s3')
websocket_api = boto3.client('apigatewaymanagementapi', endpoint_url=os.getenv('WEBSOCKET_API'))
BUCKET_NAME = os.getenv("BUCKET_NAME")


def lambda_handler(event,_context):
    route_key = event["requestContext"]["routeKey"]
    connection_id = event["requestContext"]["connectionId"]


    if route_key == '$connect':
        return {
            "statusCode": 200,
        }

    elif route_key == '$disconnect':
        return {
            "statusCode": 200,
        }

    elif route_key == 'onCheck':
        body = json.loads(event["body"])
        filename = body["filename"]
        presigned_url = check_if_ready(filename)
        status_code = 200
        msg = json.dumps(presigned_url)
        if not presigned_url:
            status_code = 404
        websocket_api.post_to_connection(
            Data = msg,
            ConnectionId = connection_id)
        return {
            "statusCode": status_code,
        }


def check_if_ready(filename):
    try:
        s3.head_object(Bucket=BUCKET_NAME, Key=filename)
        presigned_url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': filename,
            },
            ExpiresIn=300
        )
        return presigned_url
    except s3.exceptions.NoSuchKey:
        return None
    except Exception as e:
        return None
    

