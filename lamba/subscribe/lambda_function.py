import json
import boto3

sns = boto3.client("sns")

TOPIC_ARN = "arn:aws:sns:ap-southeast-1:312695118485:event-announcements"


def lambda_handler(event, context):

    try:

        # Handle CORS preflight requests
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

        # Parse request body
        body = json.loads(event["body"])

        email = body["email"]

        # Subscribe email to SNS topic
        sns.subscribe(
            TopicArn=TOPIC_ARN,
            Protocol="email",
            Endpoint=email
        )

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST, OPTIONS"
            },
            "body": json.dumps({
                "message": "Subscription request sent. Please check your email and confirm the subscription."
            })
        }

    except Exception as e:

        print("ERROR:", str(e))

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