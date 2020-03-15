import boto3
import json
from botocore.vendored import requests

dynamodb = boto3.resource('dynamodb')
# from elasticSearch import putRequests

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('match_data')


def lambda_handler(event, context):
    #   a = elasticsearch1('2019-05-01','2019-05-12')
    #   return a

    # def elasticsearch1(start_date,end_date):
    query = {
        "size": 30,
        "query": {
            "range": {
                "match_date": {
                    "gte": '2019-05-11',
                    "lte": '2019-05-12'
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

    print(result)
    return result
