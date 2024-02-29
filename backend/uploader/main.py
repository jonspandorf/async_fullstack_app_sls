import boto3 
import os
import json 

BUCKET_NAME = os.getenv("BUCKET_NAME")
QUEUE_URL = os.getenv("QUEUE_URL")
s3 = boto3.client('s3')
sqs = boto3.client('sqs')

def lambda_handler(event,_context):

    filename = event['queryStringParameters']['filename']

    try:
        presigned_url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': filename,
                'ContentType': "image/jpeg"

            },
            ExpiresIn=3600
        )
        sqs.send_message(MessageBody=json.dumps({"filename":filename}),QueueUrl=QUEUE_URL)
        return {
            'statusCode': 200,
            "isBase64Encoded": False,
            "headers": {
            "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps({'presignedUrl': presigned_url})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
