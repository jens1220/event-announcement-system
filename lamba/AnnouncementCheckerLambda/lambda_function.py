import json
import boto3
from datetime import datetime

s3 = boto3.client("s3")
sns = boto3.client("sns")

BUCKET_NAME = "event-announcement-website-1220"
EVENTS_FILE = "frontend/events.json"

TOPIC_ARN = "arn:aws:sns:ap-southeast-1:312695118485:event-announcements"


def lambda_handler(event, context):
    
    print("AnnouncementCheckerLambda started")
    print(event)

    response = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=EVENTS_FILE
    )

    events = json.loads(
        response["Body"].read().decode("utf-8")
    )

    current_time = datetime.now()

    updated = False

    for event_item in events:

        if event_item.get("announced"):
            continue

        event_datetime = datetime.strptime(
            f"{event_item['date']} {event_item['time']}",
            "%Y-%m-%d %H:%M"
        )

        if current_time >= event_datetime:

            sns.publish(
                TopicArn=TOPIC_ARN,
                Subject="Event Reminder",
                Message=f"""
Upcoming Event

Title: {event_item['title']}

Date: {event_item['date']}

Time: {event_item['time']}
"""
            )

            event_item["announced"] = True
            updated = True

    if updated:

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=EVENTS_FILE,
            Body=json.dumps(events, indent=2),
            ContentType="application/json"
        )

    return {
        "statusCode": 200,
        "body": "Check complete"
    }