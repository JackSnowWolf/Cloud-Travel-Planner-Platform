import os

import boto3

from .config import config

AWS_S3_BUCKET_NAME = config["aws"]["AWS_S3_IMG_BUCKET_NAME"]


def upload_file_to_s3(complete_file_path, filename):
    """
    Uploads a file to AWS S3. Usage:
    upload_file_to_s3('/tmp/business_plan.pdf')
    """
    if complete_file_path is None:
        raise ValueError("Please enter a valid and complete file path")

    s3 = boto3.resource('s3')
    data = open(os.path.normpath(complete_file_path), 'rb')
    # file_basename = os.path.basename(complete_file_path)
    s3.Bucket(AWS_S3_BUCKET_NAME).put_object(Key=filename, Body=data)

# Test
# upload_file_to_s3('../photos/Test2-StatueOfLiberty.jpeg', 'Test2-StatueOfLiberty.jpeg')
# logger.info("success")
