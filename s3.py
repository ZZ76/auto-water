import logging
import boto3
from botocore.exceptions import ClientError
import os
from datetime import datetime
import config

CSV_FILE = config.CSV_FILE
LOG_FILE = config.LOG_FILE 
BUCKET_NAME = config.BUCKET_NAME
AWS_REGION = config.AWS_REGION
AWS_KEY_ID = config.AWS_KEY_ID
AWS_KEY_SECRET = config.AWS_KEY_SECRET

logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s: %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=LOG_FILE, encoding='utf-8', level=logging.INFO)

s3_client = boto3.client('s3',
        region_name = AWS_REGION,
        aws_access_key_id=AWS_KEY_ID,
        aws_secret_access_key=AWS_KEY_SECRET)

def upload_file(file_name, object_name=None):
    '''Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    '''

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    try:
        response = s3_client.upload_file(file_name, BUCKET_NAME, object_name)
        #logging.info(f'Uploaded {file_name}')
        return True
    except ClientError as e:
        logging.error(f'Upload {file_name} failed, {e}')
        return False

def upload_csv():
    upload_file(CSV_FILE)
    
def upload_log():
    upload_file(LOG_FILE)

