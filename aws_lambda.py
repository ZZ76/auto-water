import logging
import boto3
from botocore.exceptions import ClientError
import io
import os
import json
import pandas as pd
import config

AWS_REGION = config.AWS_REGION
AWS_KEY_ID = config.AWS_KEY_ID
AWS_KEY_SECRET = config.AWS_KEY_SECRET
FUNCTION_NAME = config.FUNCTION_NAME

lambda_client = boto3.client('lambda',
        region_name = AWS_REGION,
        aws_access_key_id=AWS_KEY_ID,
        aws_secret_access_key=AWS_KEY_SECRET)

def test():
    payload = '{"data": "csv"}'
    response = lambda_client.invoke(FunctionName=FUNCTION_NAME, Payload=payload)
    print(response)
    print(response['Payload'])
    data_string = response['Payload'].read()
    response_json = json.loads(data_string)
    df_json_string = json.loads(response_json['body'])
    df = pd.read_json(io.StringIO(df_json_string))
    print(df)

def get_csv(lines=None):
    if lines:
        payload = f'{{"data": "csv", "lines": {lines} }}'
    else:
        payload = '{"data": "csv"}'
    response = lambda_client.invoke(FunctionName=FUNCTION_NAME, Payload=payload)
    data_string = response['Payload'].read()
    response_json = json.loads(data_string)
    df_string = response_json['body']
    df = pd.read_json(io.StringIO(df_string))
    print(df)
    return df

def get_log(lines=None):
    if lines:
        payload = f'{{"data": "log", "lines": {lines} }}'
    else:
        payload = '{"data": "log"}'
    response = lambda_client.invoke(FunctionName=FUNCTION_NAME, Payload=payload)
    data_string = response['Payload'].read()
    response_json = json.loads(data_string)
    log = response_json['body']
    print(log)
    return log

