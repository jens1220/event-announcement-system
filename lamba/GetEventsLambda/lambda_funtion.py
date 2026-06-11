import json
import boto3

s3 = boto3.client("s3")

BUCKET_NAME = "event-announcement-website-1220"
EVENTS_FILE = "frontend/events.json"

def lambda_handler(event, context):

    response = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=EVENTS_FILE
    )

    events = json.loads(
        response["Body"].read().decode("utf-8")
    )

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(events)
    }