import json
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

user_table = boto3.resource('dynamodb').Table('userTable')
schedule_table = boto3.resource('dynamodb').Table('scheduleTable')


def get_target_schedule(schedule_id):
    try:
        response = schedule_table.get_item(
            Key={
                "scheduleId": schedule_id
            }
        )

        if "Item" in response and len(response["Item"]) != 0:
            if response["Item"]["scheduleType"].upper() != "COMPLETED":
                logger.debug(json.dumps(response, indent=2))
                return True, response
        return False, {
            'statusCode': 400,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE,PATCH",
                "Access-Control-Allow-Headers": "Content-Type,Access-Control-Allow-Headers, Authorization, X-Requested-With"
            },
            'body': json.dumps({
                "code": 400,
                "msg": "schedule can not be revised"
            })
        }
    except Exception as e:
        return False, {
            'statusCode': 400,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE,PATCH",
                "Access-Control-Allow-Headers": "Content-Type,Access-Control-Allow-Headers, Authorization, X-Requested-With"
            },
            'body': json.dumps({
                "code": 400,
                "msg": "schedule id doesn't exist"
            })
        }


def get_target_user(user_id):
    try:
        response = user_table.get_item(
            Key={
                "userId": user_id
            }
        )

        if "Item" in response and len(response["Item"]) != 0:
            logger.debug(json.dumps(response, indent=2))
            return True, response
        return False, {
            'statusCode': 400,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE,PATCH",
                "Access-Control-Allow-Headers": "Content-Type,Access-Control-Allow-Headers, Authorization, X-Requested-With"
            },
            'body': json.dumps({
                "code": 400,
                "msg": "user can not be revised"
            })
        }
    except Exception as e:
        return False, {
            'statusCode': 400,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE,PATCH",
                "Access-Control-Allow-Headers": "Content-Type,Access-Control-Allow-Headers, Authorization, X-Requested-With"
            },
            'body': json.dumps({
                "code": 400,
                "msg": "user id doesn't exist"
            })
        }


def update_schedule(schedule):
    try:
        schedule_table.put_item(Item=schedule)
    except Exception as e:
        return False, {
            'statusCode': 400,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE,PATCH",
                "Access-Control-Allow-Headers": "Content-Type,Access-Control-Allow-Headers, Authorization, X-Requested-With"
            },
            'body': json.dumps({
                "code": 400,
                "msg": str(e)
            })
        }


def update_user_info(user_info):
    try:
        user_table.put_item(Item=user_info)
    except Exception as e:
        return False, {
            'statusCode': 400,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE,PATCH",
                "Access-Control-Allow-Headers": "Content-Type,Access-Control-Allow-Headers, Authorization, X-Requested-With"
            },
            'body': json.dumps({
                "code": 400,
                "msg": str(e)
            })
        }


def add_editor_to_schedule(editor_id, schedule_id):
    succ, response = get_target_schedule(schedule_id)
    if not succ:
        return response
    target_schedule = response["Item"]

    succ, response = get_target_user(editor_id)
    if not succ:
        return response
    target_user_info = response["Item"]
    if "editableSchedules" not in target_user_info:
        target_user_info["editableSchedules"] = []
    target_user_info["editableSchedules"].append(schedule_id)

    if "editorIds" not in target_schedule:
        target_schedule["editorIds"] = []
    target_schedule["editorIds"].append(editor_id)

    logger.info(target_schedule)
    logger.info(target_user_info)

    update_schedule(target_schedule)
    update_user_info(target_user_info)
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE,PATCH",
            "Access-Control-Allow-Headers": "Content-Type,Access-Control-Allow-Headers, Authorization, X-Requested-With"
        },
        'body': json.dumps({
            "code": 200,
            "schedule_type": target_schedule["scheduleType"],
            "msg": "accept invitation successfully"
        })
    }


def lambda_handler(event, context):
    # TODO implement
    try:
        logger.info("event={}".format(json.dumps(event)))
        target_schedule_id = event["pathParameters"]["scheduleId"]
        editor_id = event["queryStringParameters"]["editorId"]
        return add_editor_to_schedule(editor_id, target_schedule_id)

    except Exception as e:
        return {
            'statusCode': 400,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE,PATCH",
                "Access-Control-Allow-Headers": "Content-Type,Access-Control-Allow-Headers, Authorization, X-Requested-With"
            },
            'body': json.dumps({
                "code": 400,
                "msg": "missing required parameters!"
            })
        }



