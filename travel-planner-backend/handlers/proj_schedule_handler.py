import json
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

user_table = boto3.resource('dynamodb').Table('userTable')
schedule_table = boto3.resource('dynamodb').Table('scheduleTable')


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
            logger.debug(json.dumps(response, indent=2))
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


def get_schedule(user_id, schedule_id):
    succ, response = get_target_user(user_id)
    if not succ:
        return response
    user_info = response["Item"]
    if "editableSchedules" not in user_info or len(
            user_info["editableSchedules"]) == 0 or schedule_id not in user_info["editableSchedules"]:
        return {
            'statusCode': 403,
            'body': json.dumps({
                "code": 403,
                "msg": "Permission Denied!"
            })
        }
    succ, response = get_target_schedule(schedule_id)
    if not succ:
        return response
    return response["Item"]


def delete_schedule(user_id, schedule_id):
    succ, response = get_target_user(user_id)
    if not succ:
        return response
    user_info = response["Item"]
    try:
        user_info["editableSchedules"].remove(schedule_id)
    except Exception as e:
        logger.error(e)
        return {
            'statusCode': 403,
            'body': json.dumps({
                "code": 403,
                "msg": "Permission Denied!"
            })
        }
    delete_target_schedule(schedule_id)
    update_user_info(user_info)
    return {
        'statusCode': 200,
        'body': json.dumps({
            "code": 200,
            "msg": "Delete successfully!"
        })
    }


def post_schedule(user_id, schedule_id, schedule_content):
    succ, response = get_target_user(user_id)
    if not succ:
        return response
    user_info = response["Item"]
    if "editableSchedules" not in user_info or len(
            user_info["editableSchedules"]) == 0 or schedule_id not in user_info["editableSchedules"]:
        return {
            'statusCode': 403,
            'body': json.dumps({
                "code": 403,
                "msg": "Permission Denied!"
            })
        }
    succ, response = get_target_schedule(schedule_id)
    if not succ:
        return response
    target_schedule = response["Item"]
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
        if "scheduleId" not in event["pathStringParameters"]:
            response.update({
                'statusCode': 400,
                'body': json.dumps({
                    "code": 400,
                    "msg": "Bad Request"
                })
            })
            return response
        else:
            schedule_id = event["pathStringParameters"]["scheduleId"]
        if event["httpMethod"].upper() == "GET":
            response.update(get_schedule(user_id, schedule_id))
            return response
        if event["httpMethod"].upper() == "DELETE":
            response.update(delete_schedule(user_id, schedule_id))
            return response
        if event["httpMethod"].upper() == "POST":
            response.update(post_schedule(user_id, schedule_id, json.loads(event["body"])))
            return response
        response.update({
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "http method not supported"
            })
        })
    except Exception as e:
        response.update({
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "missing required parameters!"
            })
        })
        return response
