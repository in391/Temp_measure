import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pp-home-aws-iot-air-data')

def lambda_handler(event, context):
    try:
        data = query_recent_item()
        response = {
            'statusCode': 200,
            'body': float(data['Items'][0]['temp'])
        }
    except Exception as e:
        print(e)
        response = {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }
    return response

def query_recent_item():
    data = table.query(
                       KeyConditionExpression = boto3.dynamodb.conditions.Key('client').eq(1),
                       Limit=1,
                       ProjectionExpression = '#t',
                       ExpressionAttributeNames = {'#t': 'temp'},
                       ScanIndexForward=False)
    return data