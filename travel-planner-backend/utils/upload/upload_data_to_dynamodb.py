import json
from decimal import Decimal

import boto3

from .config import config

AWS_DB_TABLE_NAME = config["aws"]["AWS_DB_TABLE_NAME"]


def upload_data_to_dynamodb(
        attraction_id,
        attraction_name,
        attraction_description,
        attraction_area,
        attraction_loc,
        attraction_type,
        score,
        estimate_view_time,
        attraction_imgs):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(AWS_DB_TABLE_NAME)
    attraction_loc = json.loads(json.dumps(attraction_loc), parse_float=Decimal)
    score = json.loads(json.dumps(score), parse_float=Decimal)
    estimate_view_time = json.loads(json.dumps(estimate_view_time), parse_float=Decimal)
    table.put_item(
        Item={
            "attractionId": attraction_id,
            "attractionName": attraction_name,
            "attractionDescription": attraction_description,
            "attractionArea": attraction_area,
            "attractionLoc": attraction_loc,
            "attractionType": attraction_type,
            "score": score,
            "estimateViewTime": estimate_view_time,
            "attractionImgs": attraction_imgs
        }
    )
