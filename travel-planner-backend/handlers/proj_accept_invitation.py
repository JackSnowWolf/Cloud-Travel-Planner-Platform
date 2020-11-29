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

    succ, response = update_schedule(target_schedule)
    if not succ:
        return response

    succ, response = update_user_info(target_user_info)
    if not succ:
        return response
    return {
        'statusCode': 200,
        'body': json.dumps({
            "code": 200,
            "msg": "accept invitation successfully"
        })
    }


def lambda_handler(event, context):
    try:
        logger.info("event={}".format(json.dumps(event)))
        target_schedule_id = event["pathParameters"]["scheduleId"]
        editor_id = event["queryStringParameters"]["editorId"]
        return add_editor_to_schedule(editor_id, target_schedule_id)

    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "missing required parameters!"
            })
        }


if __name__ == '__main__':
    test_event = {
        "resource": "/accept/{scheduleId}",
        "path": "/accept/editing-schedule",
        "httpMethod": "GET",
        "queryStringParameters": {
            "editorId": "test-editor"
        },
        "multiValueQueryStringParameters": {
            "editorId": [
                "test-editor"
            ]
        },
        "pathParameters": {
            "scheduleId": "editing-schedule"
        }
    }
    handler_response = lambda_handler(test_event, None)
    print(json.dumps(handler_response, indent=2))
