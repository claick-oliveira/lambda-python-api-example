import boto3
import os
import json
import uuid
from datetime import datetime


def lambda_handler(message, context):

    if ('body' not in message or
            message['httpMethod'] != 'POST'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': '{\'msg\': \'Bad Request\'}'
        }

    table_name = os.environ.get('TABLE', 'Activities')
    region = os.environ.get('REGION', 'us-east-1')
    aws_environment = os.environ.get('AWSENV', 'AWS')

    if aws_environment == 'AWS_SAM_LOCAL':
        activities_table = boto3.client(
            'dynamodb',
            endpoint_url='http://dynamodb:8000'
        )
    else:
        activities_table = boto3.client(
            'dynamodb',
            region_name=region
        )

    activity = json.loads(message['body'])

    params = {
        'id': {'S': str(uuid.uuid4())},
        'date': {'S': str(datetime.timestamp(datetime.now()))},
        'status': {'S': activity['status']},
        'description': {'S': activity['description']}
    }

    response = activities_table.put_item(
        TableName=table_name,
        Item=params
    )
    print(response)

    return {
        'statusCode': 201,
        'headers': {},
        'body': '{\'msg\': \'Activity created\'}'
    }
