import json
import boto3
from datetime import datetime, timedelta

s3 = boto3.client("s3")
sns = boto3.client("sns")

BUCKET_NAME = "eas-demo-bucket"
EVENTS_FILE = "frontend/events.json"

TOPIC_ARN = "arn:aws:sns:ap-southeast-1:312695118485:EAS_SNS_Demo"


def lambda_handler(event, context):

    print("========== Announcement Checker Started ==========")

    response = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=EVENTS_FILE
    )

    events = json.loads(
        response["Body"].read().decode("utf-8")
    )

    print("Events loaded:")
    print(json.dumps(events, indent=2))

    # Philippines Time (UTC+8)
    current_time = datetime.utcnow() + timedelta(hours=8)

    print("Current Time:", current_time)

    updated = False

    for event_item in events:

        print("----------------------------------")
        print("Checking event:")
        print(event_item)

        if event_item.get("announced"):

            print("Already announced. Skipping.")
            continue

        event_datetime = datetime.strptime(
            f"{event_item['date']} {event_item['time']}",
            "%Y-%m-%d %H:%M"
        )

        print("Event Time :", event_datetime)

        if current_time >= event_datetime:

            print("Event time reached! Sending SNS...")

            response = sns.publish(
                TopicArn=TOPIC_ARN,
                Subject="Event Reminder",
                Message=f"""
Today's Event

Title: {event_item['title']}

Date: {event_item['date']}

Time: {event_item['time']}
"""
            )

            print("SNS Response:")
            print(response)

            event_item["announced"] = True
            updated = True

        else:

            print("Not time yet.")

    if updated:

        print("Updating events.json...")

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=EVENTS_FILE,
            Body=json.dumps(events, indent=2),
            ContentType="application/json"
        )

        print("events.json updated.")

    else:

        print("No updates made.")

    print("========== Finished ==========")

    return {
        "statusCode": 200,
        "body": "Check complete"
    }