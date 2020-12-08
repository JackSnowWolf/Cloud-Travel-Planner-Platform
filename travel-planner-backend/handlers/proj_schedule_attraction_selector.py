import json
import logging
from decimal import Decimal

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


def get_target_schedule(schedule_id):
    try:
        response = schedule_table.get_item(
            Key={
                "scheduleId": schedule_id
            }
        )

        if "Item" in response and len(response["Item"]) != 0:
            logger.debug(json.dumps(response["Item"], indent=2, cls=DecimalEncoder))
            if response["Item"]["scheduleType"].upper() == "PRESELECT":
                return True, response
        return False, {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "schedule can not be revised"
            })
        }
    except Exception as e:
        logger.error(e)
        return False, {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "schedule doesn't exist"
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
                "msg": "user doesn't exist"
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


def get_attraction_info_in_schedule(user_id, schedule_id, attraction_id):
    succ, response = get_target_schedule(schedule_id)
    if not succ:
        return response
    target_schedule = response["Item"]
    if user_id not in target_schedule["editorIds"] and user_id != target_schedule["ownerId"]:
        return {
            'statusCode': 403,
            'body': json.dumps({
                "code": 403,
                "msg": "Permission Denied"
            })
        }
    if "scheduleContent" in target_schedule and attraction_id in target_schedule["scheduleContent"]:
        return {
            'statusCode': 200,
            'body': json.dumps(target_schedule["scheduleContent"][attraction_id], cls=DecimalEncoder)
        }
    return {
        'statusCode': 400,
        'body': json.dumps({
            "code": 400,
            "msg": "Bad request"
        })
    }


def put_attraction_into_schedule(user_id, schedule_id, attraction_id, is_selected=None):
    succ, response = get_target_schedule(schedule_id)
    if not succ:
        return response
    target_schedule = response["Item"]
    if user_id not in target_schedule["editorIds"] and user_id != target_schedule["ownerId"]:
        return {
            'statusCode': 403,
            'body': json.dumps({
                "code": 403,
                "msg": "Permission Denied"
            })
        }
    if attraction_id in target_schedule["scheduleContent"]:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "Duplicate attraction"
            })
        }
    target_schedule["scheduleContent"][attraction_id] = {
        "isSelected": False if is_selected is None else is_selected,
        "selectedNumber": 1,
        "selectedUsers": [
            user_id
        ]
    }
    succ, response = update_schedule(target_schedule)
    if succ:
        return {
            'statusCode': 200,
            'body': json.dumps({
                "code": 200,
                "msg": "Add attraction successfully!"
            })
        }
    return response


def add_like_to_attraction(user_id, schedule_id, attraction_id, is_selected=None):
    succ, response = get_target_schedule(schedule_id)
    if not succ:
        return response
    target_schedule = response["Item"]
    if user_id not in target_schedule["editorIds"] and user_id != target_schedule["ownerId"]:
        return {
            'statusCode': 403,
            'body': json.dumps({
                "code": 403,
                "msg": "Permission Denied"
            })
        }
    if attraction_id not in target_schedule["scheduleContent"]:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "Missing attraction"
            })
        }
    attraction_info = target_schedule["scheduleContent"][attraction_id]
    if is_selected is not None:
        attraction_info.update({
            "isSelected": is_selected
        })
    if user_id not in attraction_info["selectedUsers"]:
        attraction_info["selectedUsers"].append(user_id)
        attraction_info["selectedNumber"] += 1
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "Could not add like to one attraction twice"
            })
        }
    succ, response = update_schedule(target_schedule)
    if succ:
        return {
            'statusCode': 200,
            'body': json.dumps({
                "code": 200,
                "msg": "Add like to attraction successfully!"
            })
        }
    return response


def remove_like_to_attraction(user_id, schedule_id, attraction_id, is_selected=None):
    succ, response = get_target_schedule(schedule_id)
    if not succ:
        return response
    target_schedule = response["Item"]
    if user_id not in target_schedule["editorIds"] and user_id != target_schedule["ownerId"]:
        return {
            'statusCode': 403,
            'body': json.dumps({
                "code": 403,
                "msg": "Permission Denied"
            })
        }
    if attraction_id not in target_schedule["scheduleContent"]:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "missing attraction"
            })
        }
    attraction_info = target_schedule["scheduleContent"][attraction_id]
    if is_selected is not None:
        attraction_info.update({
            "isSelected": is_selected
        })
    if user_id in attraction_info["selectedUsers"]:
        attraction_info["selectedUsers"].remove(user_id)
        attraction_info["selectedNumber"] -= 1
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "Could not remove like to one attraction twice"
            })
        }
    succ, response = update_schedule(target_schedule)
    if succ:
        return {
            'statusCode': 200,
            'body': json.dumps({
                "code": 200,
                "msg": "remove like to attraction successfully!"
            })
        }
    return response


def delete_attraction(user_id, schedule_id, attraction_id):
    succ, response = get_target_schedule(schedule_id)
    if not succ:
        return response
    target_schedule = response["Item"]
    if user_id not in target_schedule["editorIds"] and user_id != target_schedule["ownerId"]:
        return {
            'statusCode': 403,
            'body': json.dumps({
                "code": 403,
                "msg": "Permission Denied"
            })
        }
    if attraction_id not in target_schedule["scheduleContent"]:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "Missing attraction"
            })
        }
    del target_schedule["scheduleContent"][attraction_id]
    succ, response = update_schedule(target_schedule)
    if succ:
        return {
            'statusCode': 200,
            'body': json.dumps({
                "code": 200,
                "msg": "remove attraction successfully!"
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
        if "attractionId" not in event["pathParameters"]:
            response.update({
                'statusCode': 400,
                'body': json.dumps({
                    "code": 400,
                    "msg": "Bad Request"
                })
            })
            return response
        else:
            attraction_id = event["pathParameters"]["attractionId"]
        if "isSelected" in event["queryStringParameters"]:
            is_selected = event["queryStringParameters"]["isSelected"]
        else:
            is_selected = None
        if event["httpMethod"].upper() == "GET":
            response.update(get_attraction_info_in_schedule(user_id, schedule_id, attraction_id))
        elif event["httpMethod"].upper() == "PUT":
            response.update(put_attraction_into_schedule(user_id, schedule_id, attraction_id, is_selected))
        elif event["httpMethod"].upper() == "POST":
            if "like" not in event["queryStringParameters"]:
                response.update({
                    'statusCode': 400,
                    'body': json.dumps({
                        "code": 400,
                        "msg": "missing like parameter"
                    })
                })
                return response
            else:
                is_like = event["queryStringParameters"]["like"].lower() == "true"
            if is_like:
                logger.info("user add one like to an attraction")
                response.update(add_like_to_attraction(user_id, schedule_id, attraction_id, is_selected))
            else:
                logger.info("user remove one like to an attraction")
                response.update(remove_like_to_attraction(user_id, schedule_id, attraction_id, is_selected))
        elif event["httpMethod"].upper() == "DELETE":
            response.update(delete_attraction(user_id, schedule_id, attraction_id))
        else:
            response.update({
                'statusCode': 400,
                'body': json.dumps({
                    "code": 400,
                    "msg": "http method not supported"
                })
            })
        return response
    except Exception as e:
        response.update({
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "missing required parameters!"
            })
        })
        return response
