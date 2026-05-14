import boto3
import json
from dotenv import load_dotenv
import os

load_dotenv()

# --- Test S3 ---
s3 = boto3.client('s3')
buckets = s3.list_buckets()
print("✅ S3 connecté. Buckets:", [b['Name'] for b in buckets['Buckets']])

# --- Test SQS : envoyer un message ---
sqs = boto3.client('sqs')
test_message = {
    "post_id": "test_001",
    "event": "World Cup Final",
    "text": "This match is incredible!",
    "language": "en",
    "timestamp": "2026-05-13T14:30:00Z",
    "source": "simulated_twitter"
}
response = sqs.send_message(
    QueueUrl=os.getenv("SQS_QUEUE_URL"),
    MessageBody=json.dumps(test_message)
)
print("✅ SQS : message envoyé, ID:", response['MessageId'])

# --- Test SQS : recevoir le message ---
msgs = sqs.receive_message(
    QueueUrl=os.getenv("SQS_QUEUE_URL"),
    MaxNumberOfMessages=1
)
if 'Messages' in msgs:
    body = json.loads(msgs['Messages'][0]['Body'])
    print("✅ SQS : message reçu:", body['text'])

# --- Test S3 : uploader un fichier ---
s3.put_object(
    Bucket=os.getenv("S3_BUCKET"),
    Key="event=world_cup/date=2026-05-13/test_post.json",
    Body=json.dumps(test_message)
)
print("✅ S3 : fichier uploadé avec succès")