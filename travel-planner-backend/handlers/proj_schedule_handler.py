import json
import logging
from decimal import Decimal
from functools import reduce
from operator import iconcat

import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

user_table = boto3.resource('dynamodb').Table('userTable')
schedule_table = boto3.resource('dynamodb').Table('scheduleTable')


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


def get_target_user(user_id):
    try:
        response = user_table.get_item(
            Key={
                "userId": user_id
            }
        )

        if "Item" in response and len(response["Item"]) != 0:
            # logger.debug(json.dumps(response, indent=2))
            return True, response
        return False, {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "user can not be revised"
            })
        }
    except Exception as e:
        return False, {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "user id doesn't exist"
            })
        }


def get_target_schedule(schedule_id):
    try:
        response = schedule_table.get_item(
            Key={
                "scheduleId": schedule_id
            }
        )

        if "Item" in response and len(response["Item"]) != 0:
            logger.debug(json.dumps(response, indent=2, cls=DecimalEncoder))
            return True, response
        return False, {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "schedule can not be revised"
            })
        }
    except Exception as e:
        return False, {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "schedule id doesn't exist"
            })
        }


def update_schedule(schedule):
    try:
        schedule_table.put_item(Item=schedule)
        return True, None
    except Exception as e:
        return False, {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": str(e)
            })
        }


def update_user_info(user_info):
    try:
        schedule_table.update_item(Item=user_info)
    except Exception as e:
        return False, {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": str(e)
            })
        }


def delete_target_schedule(schedule_id):
    try:
        schedule_table.delete_item(Key={
            "scheduleId": schedule_id
        })
        return True, None
    except Exception as e:
        return False, {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": str(e)
            })
        }


def extract_item(item):
    bucket = item["bucket"]
    object_key = item["objectKey"]
    return "https://{:s}.s3.amazonaws.com/{:s}".format(bucket, object_key)


def extract_attraction(attraction_info):
    attraction_img_urls = list(map(extract_item, attraction_info["attractionImgs"]))
    del attraction_info["attractionImgs"]
    attraction_info["attractionImgUrls"] = attraction_img_urls
    return attraction_info


def batch_get_user_info(user_id_list):
    try:
        response = boto3.resource('dynamodb').batch_get_item(
            RequestItems={
                "userTable": {
                    "Keys": list(map(lambda user_id: {"userId": user_id}, user_id_list)),
                    "AttributesToGet": [
                        "userId",
                        "editableSchedules"
                    ]
                }
            }
        )

        if "Responses" in response and len(response["UnprocessedKeys"]) == 0:
            return True, response["Responses"]
        return False, {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "can not get user info"
            })
        }
    except Exception as e:
        logger.error(e)
        return False, {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "user id doesn't exist"
            })
        }


def update_user_info_editable_schedules(user_info):
    try:
        user_table.update_item(
            Key={"userId": user_info["userId"]},
            UpdateExpression="set editableSchedules=:s",
            ExpressionAttributeValues={
                ":s": user_info["editableSchedules"]
            })
        return True, None
    except Exception as e:
        logger.error(e)
        return False, {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": str(e)
            })
        }


def batch_get_attraction(attraction_id_list):
    try:
        response = boto3.resource('dynamodb').batch_get_item(
            RequestItems={
                "attractionTable": {
                    "Keys": list(map(lambda attraction_id: {"attractionId": attraction_id}, attraction_id_list)),
                }
            }
        )

        if "Responses" in response and len(response["UnprocessedKeys"]) == 0:
            return True, response["Responses"]
        return False, {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "can not get attraction attributes"
            })
        }
    except Exception as e:
        logger.error(e)
        return False, {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "attraction id doesn't exist"
            })
        }


def get_preselect_schedule(target_schedule):
    attraction_id_list = list(target_schedule["scheduleContent"].keys())
    if attraction_id_list is None or len(attraction_id_list) == 0:
        logger.debug("No attractions in the schedule")
        return True, target_schedule
    succ, response = batch_get_attraction(set(attraction_id_list))
    if not succ:
        return False, response
    attraction_info_list = response["attractionTable"]
    attraction_extracted_info_list = list(map(extract_attraction, attraction_info_list))
    for info in attraction_extracted_info_list:
        target_schedule["scheduleContent"][info["attractionId"]].update(info)
    return True, target_schedule


def get_complete_schedule(target_schedule):
    list_of_attrlist = []
    for dayContent in target_schedule["scheduleContent"]["dayScheduleContents"]:
        list_of_attrlist.append(dayContent["Details"])

    attraction_id_list= [item for elem in list_of_attrlist for item in elem]
    # attraction_id_list = reduce(iconcat, list_of_attrlist)

    if attraction_id_list is None or len(attraction_id_list) == 0:
        logger.debug("No attractions in the schedule")
        return True, target_schedule
    succ, response = batch_get_attraction(set(attraction_id_list))
    if not succ:
        return False, response
    attraction_info_list = response["attractionTable"]
    attraction_extracted_info_list = list(map(extract_attraction, attraction_info_list))
    attraction_info_map = dict(zip(list(map(lambda attraction_info: attraction_info["attractionId"],
                                            attraction_extracted_info_list)),
                                   attraction_info_list))
    for ind, day_schedule_content in enumerate(target_schedule["scheduleContent"]["dayScheduleContents"]):
        target_schedule["scheduleContent"]["dayScheduleContents"][ind]["Details"] = list(map(lambda attraction_id:
                                                                                             attraction_info_map[
                                                                                                 attraction_id],
                                                                                             day_schedule_content[
                                                                                                 "Details"]))
    return True, target_schedule


def get_schedule(user_id, schedule_id):
    succ, response = get_target_schedule(schedule_id)
    if not succ:
        return response
    target_schedule = response["Item"]
    if user_id not in target_schedule["editorIds"] and user_id != target_schedule["ownerId"]:
        return {
            'statusCode': 403,
            'body': json.dumps({
                "code": 403,
                "msg": "Permission Denied!"
            })
        }
    if target_schedule["scheduleType"].upper() == "PRESELECT":
        succ, response = get_preselect_schedule(target_schedule)
        if not succ:
            return response
    else:
        succ, response = get_complete_schedule(target_schedule)
        if not succ:
            return response
    return {
        'statusCode': 200,
        'body': json.dumps(target_schedule, cls=DecimalEncoder)
    }


def delete_schedule(user_id, schedule_id):
    succ, response = get_target_schedule(schedule_id)
    if not succ:
        return response
    target_schedule = response["Item"]
    if user_id != target_schedule["ownerId"]:
        return {
            'statusCode': 403,
            'body': json.dumps({
                "code": 403,
                "msg": "Permission Denied!"
            })
        }

    editor_list = target_schedule.get("editorIds", [])
    editor_list.append(target_schedule["ownerId"])
    succ, response = batch_get_user_info(editor_list)
    if not succ:
        return response
    editor_user_info_list = response["userTable"]
    for editor_user_info in editor_user_info_list:
        if schedule_id in editor_user_info["editableSchedules"]:
            editor_user_info["editableSchedules"].remove(schedule_id)
            update_user_info_editable_schedules(editor_user_info)

    succ, response = delete_target_schedule(schedule_id)
    if not succ:
        return response
    return {
        'statusCode': 200,
        'body': json.dumps({
            "code": 200,
            "msg": "Delete successfully!"
        })
    }


def post_schedule(user_id, schedule_id, schedule_content):
    succ, response = get_target_schedule(schedule_id)
    if not succ:
        return response
    target_schedule = response["Item"]
    if user_id not in target_schedule["editorIds"] and user_id != target_schedule["ownerId"]:
        return {
            'statusCode': 403,
            'body': json.dumps({
                "code": 403,
                "msg": "Permission Denied!"
            })
        }
    if target_schedule["scheduleType"].upper() != "EDITING":
        return {
            'statusCode': 403,
            'body': json.dumps({
                "code": 403,
                "msg": "Permission Denied!"
            })
        }
    target_schedule["scheduleContent"] = schedule_content
    succ, response = update_schedule(target_schedule)
    if succ:
        return {
            'statusCode': 200,
            'body': json.dumps({
                "code": 200,
                "msg": "Update successfully!"
            })
        }
    return response


def patch_schedule(user_id, schedule_id, day_schedule_content):
    succ, response = get_target_schedule(schedule_id)
    if not succ:
        return response
    target_schedule = response["Item"]
    if user_id not in target_schedule["editorIds"] and user_id != target_schedule["ownerId"]:
        return {
            'statusCode': 403,
            'body': json.dumps({
                "code": 403,
                "msg": "Permission Denied!"
            })
        }
    if target_schedule["scheduleType"].upper() != "EDITING":
        return {
            'statusCode': 403,
            'body': json.dumps({
                "code": 403,
                "msg": "Permission Denied!"
            })
        }

    try:
        data_to_change = int(day_schedule_content["NumDate"][3:])
    except Exception as e:
        logger.error(e)
        return {
            'statusCode': 403,
            'body': json.dumps({
                "code": 403,
                "msg": "No or Invalid NumDate!"
            })
        }
    operated_data = day_schedule_content["Details"]
    target_schedule["scheduleContent"]["dayScheduleContents"][data_to_change - 1]["Details"]=operated_data

    succ, response = update_schedule(target_schedule)
    if succ:
        return {
            'statusCode': 200,
            'body': json.dumps({
                "code": 200,
                "msg": "Update successfully!"
            })
        }
    return response


def lambda_handler(event, context):
    response = {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE,PATCH",
            "Access-Control-Allow-Headers": "Content-Type,Access-Control-Allow-Headers, Authorization, X-Requested-With"
        }
    }
    try:
        logger.info("event={}".format(json.dumps(event)))
        if "userId" not in event["queryStringParameters"]:
            response.update({
                'statusCode': 401,
                'body': json.dumps({
                    "code": 401,
                    "msg": "unauthorized request"
                })
            })
            return response
        else:
            user_id = event["queryStringParameters"]["userId"]
        if "scheduleId" not in event["pathParameters"]:
            response.update({
                'statusCode': 400,
                'body': json.dumps({
                    "code": 400,
                    "msg": "Bad Request"
                })
            })
            return response
        else:
            schedule_id = event["pathParameters"]["scheduleId"]
        if event["httpMethod"].upper() == "GET":
            response.update(get_schedule(user_id, schedule_id))
            return response
        if event["httpMethod"].upper() == "DELETE":
            response.update(delete_schedule(user_id, schedule_id))
            return response
        if event["httpMethod"].upper() == "POST":
            response.update(post_schedule(user_id, schedule_id, json.loads(event["body"])))
            return response
        if event["httpMethod"].upper() == "PATCH":
            response.update(patch_schedule(user_id, schedule_id, json.loads(event["body"])))
            return response
        response.update({
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "http method not supported"
            })
        })
    except Exception as e:
        logger.error(e)
        response.update({
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "missing required parameters!"
            })
        })
        return response
