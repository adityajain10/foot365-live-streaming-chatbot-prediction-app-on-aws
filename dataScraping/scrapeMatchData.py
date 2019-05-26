import json
from botocore.vendored import requests
from urlparse import urljoin
import boto3
import json
from decimal import *
import datetime
from time import sleep
from decimal import *
s3_client=boto3.client('s3')
dynamodb=boto3.resource('dynamodb')
#from elasticSearch import putRequests

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('standings007')

#def scrape():
def lambda_handler(event, context):
    bucket=event['Records'][0]['s3']['bucket']['name']
    json_file_name=event['Records'][0]['s3']['object']['key']
    print(bucket)
    print(json_file_name)
    print(str(event))
    json_object=s3_client.get_object(Bucket=bucket,Key=json_file_name)
    jsonFileReader=json_object['Body'].read()
    #print('check now')
    jsonDict=json.loads(jsonFileReader)
    count=0
    for data in jsonDict:
        #print(jsonDict[i])
        dict={}
        dict['team_name']=str(data['team_name'])
        dict['overall_league_position']=str(data['overall_league_position'])
        dict['overall_league_payed']=str(data['overall_league_payed'])
        dict['overall_league_W']=str(data['overall_league_W'])
        dict['overall_league_D']=str(data['overall_league_D'])
        dict['overall_league_L']=str(data['overall_league_L'])
        dict['overall_league_GF']=str(data['overall_league_GF'])
        dict['overall_league_GA']=str(data['overall_league_GA'])
        dict['overall_league_PTS']=str(data['overall_league_PTS'])
        table.put_item(Item=dict)
        count=count+1
    print(count)
    return 'ram'

#def lambda_handler(event, context):
    # TODO implement
   # putRequests()
   # return {
    #    'statusCode': 200,
    #    'body': json.dumps('Hello from Lambda!')
  # }