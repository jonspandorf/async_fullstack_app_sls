import boto3
import cv2
import os  
import json

BUCKET_NAME = os.getenv("BUCKET_NAME")
QUEUE_URL = os.getenv("QUEUE_URL")

s3 = boto3.client('s3')
sqs = boto3.client('sqs')

def lambda_handler(event,_context):
    status_code = 200
    client_res_msg = "Records processed!!!"
    handled_msgs = list()
    try:
        for record in event['Records']:
            print(f"Handling message {record['receiptHandle']}")
            msg = json.loads(record['body'])
            handled_msgs.append(record['receiptHandle'])
            bucket_key = msg['filename']
            print(f"Searching for file {bucket_key.split('.')[0]}")
            filepath = get_image_from_bucket(bucket_key)
            print(f"Processing image {filepath}")
            processed_path = process_image(filepath)
            print("File processed sucessfully!\nUploading artifact to bucket")
            s3.upload_file(processed_path, BUCKET_NAME, bucket_key+'Processed')
            print(f"Removing from key {bucket_key} from bucket")
            s3.delete_object(Bucket=BUCKET_NAME, Key=bucket_key)
        delete_messages(handled_msgs)
    except s3.exceptions.ClientError as e: 
        print(f"File not found Error!!! {str(e)}")
        if e.response['Error']['Code'] == '404':
            status_code = 404 
            client_res_msg = "File is still being upload"
    except Exception as e: 
        print(f"Error!!! {str(e)}")
        msg = str(e)
        status_code = 500 
        delete_messages(handled_msgs)

    return {
        'statusCode': status_code,
        'body': json.dumps(client_res_msg)
    }

def delete_messages(handled_msgs):      
    for receipt in handled_msgs:
        print(f"Deleting message")
        sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=receipt)

def get_image_from_bucket(bucket_key):
    filepath = '/tmp/' + os.path.basename(bucket_key)
    print(f"Downloading file to {filepath}")
    s3.download_file(BUCKET_NAME, bucket_key, filepath)
    print("File Downloaded Sucessfully!")
    return filepath

def process_image(filepath):
    try:
        # Load the cascade
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        # Read the input image
        img = cv2.imread(filepath)
        # Convert into grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.023, 4)
        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        processed_filename = filepath.split('.')[0]+'Processed.jpg'
        cv2.imwrite(processed_filename, img)
        return processed_filename
    except Exception as e:
        raise(e)
    
