import json
import boto3

sns = boto3.client("sns")

TOPIC_ARN = "arn:aws:sns:ap-southeast-1:312695118485:event-announcements"


def lambda_handler(event, context):

    try:

        body = json.loads(event["body"])

        email = body["email"]

        sns.subscribe(
            TopicArn=TOPIC_ARN,
            Protocol="email",
            Endpoint=email
        )

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Subscription request sent. Check your email and confirm the subscription."
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