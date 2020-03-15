import random
import json
import boto3
import datetime
from botocore.vendored import requests

# API_KEY= 'm68Jb9xYu4eUQH0RKbjlFGOj6lzCEEdExprjLAj3Bw8inSDYbODwF1EO13wr1QXaz68XUeoB-Ay-yxwaC4y1KqqHOWc6towlxTvyAXKooWHtYAepY4okWAbeP1SlXHYx'

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('match_data')


def lambda_handler(event, context):
    pollSNS()
    # print('\n',yelpResult)
    # insertIntoDynamo()


def pollSNS():
    # create a boto3 client

    client = boto3.client('sqs')
    sms_client = boto3.client('sns')

    # create the test queue
    # for a FIFO queue, the name must end in .fifo, and you must pass FifoQueue = True
    # client.create_queue(QueueName='dinningQueue')
    # get a list of queues, we get back a dict with 'QueueUrls' as a key with a list of queue URLs

    queues = client.list_queues(QueueNamePrefix='StandardSQS')  # we filter to narrow down the list
    test_queue_url = queues['QueueUrls'][0]

    while True:
        # response = client.receive_message(QueueUrl=test_queue_url,AttributeNames=['ALL'],MaxNumberOfMessages=5) # adjust MaxNumberOfMessages if needed
        # Receive message from SQS queue
        response = client.receive_message(
            QueueUrl=test_queue_url,
            AttributeNames=[
                'All'
            ],
            MaxNumberOfMessages=10,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=30,
            WaitTimeSeconds=0
        )
        msg = ''

        if 'Messages' in response:  # when the queue is exhausted, the response dict contains no 'Messages' key
            for message in response['Messages']:  # 'Messages' is a list
                js = json.loads(message['Body'])
                # print(json.dumps(js,indent=4,sort_keys=True))
                start_date = js['start_date']
                end_date = js['end_date']
                phone = js['phone']
                print("start date" + start_date)
                print("end date" + end_date)
                result = elasticsearch1(start_date, end_date)
                # msg += "Match between "+ str(result["match_hometeam_name"]) +" vs "+ str(result["match_awayteam_name"]) + " on " + str(result["match_date"])+"\n"
                client.delete_message(QueueUrl=test_queue_url, ReceiptHandle=message['ReceiptHandle'])
            print(msg)

            print(type(result))
            mess = "thank you for using foot365. The fixtures are as per following:\n"
            for i in result:
                mess = mess + str(i) + "\n"
            print(mess)
            check = sms_client.publish(PhoneNumber=phone, Message=mess)
            # print(str(check))

        else:
            print('Queue is now empty')
            break


def elasticsearch1(start_date, end_date):
    query = {
        "size": 20,
        "query": {
            "range": {
                "match_date": {
                    "gte": start_date,
                    "lte": end_date
                }
            }
        }
    }
    headers = {"Content-Type": "application/json"}
    url = 'https://search-match007-32fnph2szbin7xcsklg2gksgky.us-east-1.es.amazonaws.com/match007/match/_search'
    r = requests.get(url, headers=headers, data=json.dumps(query))
    r = json.loads(r.text)
    # n=r['hits']["total"][1]['_source']
    nums_hit = r['hits']["total"]
    print("nums hit" + str(nums_hit))
    result = []
    if nums_hit == 0:
        print("No Match is there")
    elif nums_hit <= 20:
        for i in range(0, nums_hit):
            result.append(r['hits']['hits'][i]['_source'])
    elif nums_hit > 20:
        for i in range(0, 20):
            result.append(r['hits']['hits'][i]['_source'])
    else:
        print("unknown eror")
    return result
