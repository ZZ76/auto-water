import json
import boto3
import io
from io import StringIO
import pandas as pd

BUCKET_NAME = 's3-bucket-name'

def get_csv(lines=None, response='json'):
    # s3
    s3_client = boto3.client('s3')
    data_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key='data.csv')
    csv_string = data_obj["Body"].read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_string))
    if lines:
        if lines > 0:
            df = df[:lines]
        else:
            df = df[lines:]
    if response != 'json':
        return df.to_string()
    return df.to_json()
    # print(df_json)
    # return df_json

def get_log(l=None):
    # s3
    s3_client = boto3.client('s3')
    data_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key='log')
    content = data_obj["Body"].read().decode('utf-8')
    if l:
        with StringIO(content) as string_buffer:
            lines = string_buffer.readlines()
            if l > 0:
                content = ''.join(lines[:l])
            else:
                content = ''.join(lines[l:])
                # content = lines[l:]
    # df_json = df.to_json()
    # print(df_json)
    return content

def lambda_handler(event, context):
    # TODO implement
    print(event)
    print(event.keys())

    data = 'log'
    lines = 0
    result = None
    response = 'json'

    if 'data' in event.keys():
        print(event['data'])
        data = event['data']
        if 'lines' in event.keys():
            lines = int(event['lines'])

    elif 'queryStringParameters' in event.keys():
        print(event['queryStringParameters'])
        data = event['queryStringParameters']['data']
        response = 'string'
        if 'lines' in event['queryStringParameters'].keys():
            lines = int(event['queryStringParameters']['lines'])

    if data == 'csv':
        if lines != 0 :
            result = get_csv(lines=lines, response=response)
        else:
            result = get_csv(lines=lines, response=response)
    elif data == 'log':
        if lines != 0 :
            result = get_log(l=lines)
        else:
            result = get_log()

    return {
        'statusCode': 200,
        'body': result,
    }
