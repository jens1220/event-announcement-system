# Event-Announcement-system

A notification system that will sent to the Email Users by given time and date.
![image alt](https://github.com/jens1220/Space-Website1220/blob/main/screenshot/Website.PNG?raw=true)

## 🚀 Features
- Feature 1: Email Subscription with AWS SNS.
- Feature 2: Event Creation with time and date setup.
- Feature 3: Notification system for the Email Subscription.

## 🛠️ Installation

Create a repository in Github then upload your project folder with git commands.

1. Navigate to your folder first before you do the command:
   ```bash
   cd folder/projectname
2. Commands list by order
   ```bash
   git remote add origin https://github.com/yourUserName/RepositoryName.git
   git add .
   git commit -m "Project Upload"
   git branch -m main
   git push -u origin main
3. Create S3 Bucket
   - Uncheck block public access setting
   - add bucket policy
   ```json
   {
	"Version": "2012-10-17",
		"Statement": [
			{
				"Sid": "PublicReadGetObject",
				"Effect": "Allow",
				"Principal": "*",
				"Action": "s3:GetObject",
				"Resource": "arn:aws:s3:::yourbucketARN/*"
			}
		]
   }
   ```
   - Assign a defualt page in website hosting in properties

   ![image alt](https://github.com/jens1220/Space-Website1220/blob/main/screenshot/S3%20Static%20website.png?raw=true)
   
4. Create custom pipeline
   - Connect to your github repository
   - Use codebuild for buildspec.yml

   ![image alt](https://github.com/jens1220/Space-Website1220/blob/main/screenshot/CP01.PNG?raw=true)
   ![image alt](https://github.com/jens1220/Space-Website1220/blob/main/screenshot/CP02.PNG?raw=true)
   ![image alt](https://github.com/jens1220/Space-Website1220/blob/main/screenshot/CP03.PNG?raw=true)
   ![image alt](https://github.com/jens1220/Space-Website1220/blob/main/screenshot/CP04.PNG?raw=true)
   ![image alt](https://github.com/jens1220/Space-Website1220/blob/main/screenshot/CICD.PNG?raw=true)
   
   - After you establish your website create new file **events.json** and add code
   ```json
       [
     {
      "title": "Test Event",
      "date": "2026-06-14",
      "time": "16:56",
      "announced": true
     }
   ]
   ```
   git push the file or manually upload it to S3 inside the frontend. make sure delete(events.json) it to your local to avoid getting overwritten the S3 every time you do **git push**
4. Create SNS
   - Type: Standard
5. Create Subscribe Lambda
   - Purpose: Receive Email subscription
   - add IAM permission(AmazonSNSFullAccess)
   - Add Code (in the Project folder > Subscribe.py copy and paste it in lambda's code section)
   - Incase APIGW didn't add resource base policy(Principal:apigateway.amazonaws.com and Action:lambda:InvokeFunction)
6. Create Event lambda
   - Purpose: Save the created event from website
   - Add code (in the Project folder > create-event.py copy and paste it in lambda's code section)
   - add IAM permission (AmazonS3FullAccess and AmazonSNSFullAccess)
   - Incase APIGW didn't add resource base policy(Principal:apigateway.amazonaws.com and Action:lambda:InvokeFunction)
7. Create get GetEventsLambda
   - Purpose: Display the upcoming event
   - (in the Project folder > GetEventsLambda.py copy and paste it in lambda's code section)
   - add IAM permission (AmazonS3FullAccess)
   - Incase APIGW didn't add resource base policy(Principal:apigateway.amazonaws.com and Action:lambda:InvokeFunction)
8. API gateway Setup
   - subscribe/**POST** and create-event/**POST** also enable Lambda proxy integration and link them to the corresponding lambda
   - enable CORS for both
   - In CORS Section Access-Control-Allow-Headers: **Content-Type**
   - also Create event/**GET** and link it to GetEventsLambda

   ![image alt](https://github.com/jens1220/Space-Website1220/blob/main/screenshot/API%20GATEWAY.PNG?raw=true).

9. Create Announcement checker Lambda
   - Purpose: Check whether an event should be announced.
   - Add IAM Permission (AmazonS3FullAccess and AmazonSNSFullAccess)
   - add code (in the Project folder > AnnouncementcheckerLambda.py copy and paste it in lambda's code section)
   - Incase APIGW didn't add resource base policy(Principal:scheduler.amazonaws.com and Action:lambda:InvokeFunction)
11. Create eventbridge Scheduler
   - Check events automatically for ontime announcement
   - Schedule type: Rate-based schedule
   - Value:1 Unit:Minute
   - Target: AWS Lambda Invoke > AnnouncementCheckerLambda
   - Allow: Schedule Enable
12. Test the website now go to **S3**> frontend > index.html > **Below the Object URL** Click the link and try the website
#Email Notification preview
![image alt](https://github.com/jens1220/Space-Website1220/blob/main/screenshot/Message.PNG?raw=true)
