import boto3


# Helper class to convert a DynamoDB item to JSON.

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('livescore')

    result = table.scan()
    data = result['Items']

    while 'LastEvaluatedKey' in result:
        result = table.scan(ExclusiveStartKey=result['LastEvaluatedKey'])
        data.extend(result['Items'])

    result = []
    for i in data:
        result.append(i)

    print(len(result))
    print(result)
    return result
