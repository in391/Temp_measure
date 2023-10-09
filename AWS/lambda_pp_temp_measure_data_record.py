import boto3
import json
import traceback
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pp-temp-measure-data')

def lambda_handler(event, context):
    try:
        if(len(event['value']) == 1):
            put_one_item(event['value'][0])
        elif(len(event['value']) > 1):
            put_multi_items(event['value'])
        else:
            raise TypeError
    except TypeError as e:
        print(e)
        response = {
            'statusCode': 400,
            'body': json.dumps('Type Error or Empty List')
        }
    except Exception as e:
        print(e)
        response = {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }
    else:
        response = {
            'statusCode': 200,
            'body': json.dumps('Successfully Created')
        }
    return response

def put_one_item(event):
    data = table.put_item(
        Item = {
            'Timestamp': event['Timestamp'],
            'Client': event['Client'],
            'Temp': Decimal(event['Temp']),
            'Humid': Decimal(event['Humid']),
            'Gas': Decimal(event['Gas'])
        }
    )
    return data
    
def put_multi_items(event):
    with table.batch_writer() as batch:
        for it in event:
            batch.put_item(
                Item = {
                    'Timestamp': it['Timestamp'],
                    'Client': it['Client'],
                    'Temp': Decimal(it['Temp']),
                    'Humid': Decimal(it['Humid']),
                    'Gas': Decimal(it['Gas'])
                }
            )
    return