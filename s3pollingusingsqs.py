import os
import boto3
import schedule
import time
import datetime

def writeoutput():

    commandtext = os.popen('dir').read()

    s3 = boto3.resource(
        's3',
        region_name='us-east-1',
        aws_access_key_id='',
        aws_secret_access_key=''
    )
    s3.Object('hccake', 'watchfolder/response.txt').put(Body=commandtext)


def putmessageinqueue():
    sqs = boto3.resource(
        'sqs',
        aws_access_key_id='',
        aws_secret_access_key=''
        )
    queue = sqs.get_queue_by_name(QueueName='testqueue')
    response = queue.send_message(MessageBody='filename')
    print(response.get('MessageId'))

def readmessageinqueue():
    sqs = boto3.resource(
        'sqs',
        aws_access_key_id='',
        aws_secret_access_key=''
    )
    queue = sqs.get_queue_by_name(QueueName='testqueue')
    messages = queue.receive_messages(WaitTimeSeconds=1)
    for message in messages:
        print(message.body)
        message.delete()

def domyjob():
    putmessageinqueue()
    readmessageinqueue()
    writeoutput()

schedule.every(1).minutes.do(domyjob)

while True:
    schedule.run_pending() 
    time.sleep(1) 
