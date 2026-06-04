import json
import boto3

s3 = boto3.client("s3")
sns = boto3.client("sns")

BUCKET_NAME = "event-announcement-website"
EVENTS_FILE = "events.json"

TOPIC_ARN = "YOUR_SNS_TOPIC_ARN"


def lambda_handler(event, context):

    try:

        body = json.loads(event["body"])

        title = body["title"]
        date = body["date"]
        time = body["time"]

        response = s3.get_object(
            Bucket=BUCKET_NAME,
            Key=EVENTS_FILE
        )

        events = json.loads(
            response["Body"]
            .read()
            .decode("utf-8")
        )

        new_event = {
            "title": title,
            "date": date,
            "time": time
        }

        events.append(new_event)

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=EVENTS_FILE,
            Body=json.dumps(
                events,
                indent=2
            ),
            ContentType="application/json"
        )

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
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Event created successfully"
            })
        }

    except Exception as e:

        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }
