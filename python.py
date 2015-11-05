#!/usr/bin/python

###Libraries
import sys
import boto3
import os
import MySQLdb
import time

###Variables
s3bucket = os.environ['APP_S3_BUCKET']
SQS_url = os.environ['APP_SQS_URL']
APP_DB_HOST = os.environ['APP_DB_HOST']
APP_DB_DATABASE = os.environ['APP_DB_DATABASE']
APP_DB_PORT = int(os.environ['APP_DB_PORT'])
APP_DB_USERNAME = os.environ['APP_DB_USERNAME']
APP_DB_PASSWORD = os.environ['APP_DB_PASSWORD']
APP_AWS_REGION = os.environ['APP_AWS_REGION']
os.environ["AWS_ACCESS_KEY_ID"] = os.environ['APP_AWS_ACCESS_KEY']
os.environ["AWS_SECRET_ACCESS_KEY"] = os.environ['APP_AWS_SECRET_KEY']

sqs = boto3.client('sqs', region_name = APP_AWS_REGION)
s3 = boto3.client('s3')
db = MySQLdb.connect(host=APP_DB_HOST,
                     port=APP_DB_PORT,
                     user=APP_DB_USERNAME,
                     passwd=APP_DB_PASSWORD,
                     db=APP_DB_DATABASE,
                     use_unicode=True,
                     charset='utf8')
cursor = db.cursor()

print "Beginning loop..."
###Main Function
def sqs_downloader():
	print "Checking sqs queue for new messages..."
	response = sqs.receive_message(QueueUrl = SQS_url)
	if 'Messages' in response:
		print "New message found!"
		for message in response['Messages']:
			body = message['Body']
			receipt = message['ReceiptHandle']
			print "New file found in queue.  Downloading " + body
			s3.download_file(s3bucket, body, '/tmp/' + body)
			print "File saved as /tmp/" + body + ".  Executing sql import..."
			for line in open('/tmp/' + body):
				cursor.execute(line.decode("utf-8-sig"))
			db.commit()
			sqs.delete_message(QueueUrl = SQS_url, ReceiptHandle=receipt)
	else:
		print "Nothing to import.  Sleeping for 30 seconds."
		time.sleep(30)
		
###Begin actual script - we run sqs_downloader function over and over until the end of time.
while True:
	sqs_downloader()