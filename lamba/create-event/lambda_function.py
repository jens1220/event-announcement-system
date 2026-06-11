import json
import boto3

s3 = boto3.client("s3")
sns = boto3.client("sns")

BUCKET_NAME = "event-announcement-website-1220"
EVENTS_FILE = "frontend/events.json"

TOPIC_ARN = "arn:aws:sns:ap-southeast-1:312695118485:event-announcements"


def lambda_handler(event, context):

    try:

        # Handle CORS preflight request
        if event.get("httpMethod") == "OPTIONS":

            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "POST, OPTIONS"
                },
                "body": ""
            }

        body = json.loads(event["body"])

        title = body["title"]
        date = body["date"]
        time = body["time"]

        # Keep only the newest event
        events = [
            {
                "title": title,
                "date": date,
                "time": time
            }
        ]

        # Overwrite events.json
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=EVENTS_FILE,
            Body=json.dumps(events, indent=2),
            ContentType="application/json"
        )

        # Send SNS notification
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject="New Event Created",
            Message=f"""
New Event Announcement

Title: {title}

Date: {date}

Time: {time}
"""
        )

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST, OPTIONS"
            },
            "body": json.dumps({
                "message": "Event created successfully"
            })
        }

    except Exception as e:

        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST, OPTIONS"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }