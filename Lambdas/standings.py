import boto3
import json


# Helper class to convert a DynamoDB item to JSON.

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('standings007')

    result = table.scan()
    data = result['Items']

    while 'LastEvaluatedKey' in result:
        result = table.scan(ExclusiveStartKey=result['LastEvaluatedKey'])
        data.extend(result['Items'])

    result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in data:
        temp = int(i['overall_league_position'])
        result[temp - 1] = i
    res = json.dumps(result)
    print(result)
    return result
