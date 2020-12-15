import json
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

user_table = boto3.resource('dynamodb').Table('userTable')
schedule_table = boto3.resource('dynamodb').Table('scheduleTable')
attraction_table = boto3.resource('dynamodb').Table('attractionTable')


def get_target_schedule(schedule_id):
    try:
        response = schedule_table.get_item(
            Key={
                "scheduleId": schedule_id
            }
        )

        if "Item" in response and len(response["Item"]) != 0:
            # logger.debug(json.dumps(response, indent=2))
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
                "msg": "schedule doesn't exist"
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


def submit_schedule(user_id, schedule_id):
    succ, response_schedule = get_target_schedule(schedule_id)
    if not succ:
        return response_schedule
    target_schedule = response_schedule["Item"]
    if target_schedule["scheduleType"].upper() != "PRESELECT":
        return {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "Can not submit schedule with non-PRESELECT type"
            })
        }
    if user_id != target_schedule["ownerId"]:
        return {
            'statusCode': 403,
            'body': json.dumps({
                "code": 403,
                "msg": "Permission Denied"
            })
        }

    # TODO: arrange schedule

    schedule_content = {
        "metaData": "dummy"
    }
    dayschedule_contents = []
    dayone = {
        "NumDate": "day1"
    }
    daytwo = {
        "NumDate": "day2"
    }
    preselect_attr_list = list(target_schedule["scheduleContent"].keys())
    preselect_attr_first = str(preselect_attr_list[0])
    response_list = attraction_table.scan(ProjectionExpression="attractionId,score")
    attr_score_item_list = response_list["Items"]
    attr_score_item_list.sort(key=lambda a: -a["score"])
    pop_attr_list_db = list(map(lambda a: str(a["attractionId"]), attr_score_item_list))
    pop_attr_list_db.insert(0, preselect_attr_first)
    pop_attr_list = list(dict.fromkeys(pop_attr_list_db))

    # By default: 2 day and 6 attractions max
    if len(pop_attr_list) <= 0:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "No attraction"
            })
        }
    elif len(pop_attr_list) <= 3:
        dayone.update({
            "Details": pop_attr_list
        })
        dayschedule_contents.append(dayone)
    elif len(pop_attr_list) <= 6:
        dayone.update({
            "Details": pop_attr_list[0:3]
        })
        daytwo.update({
            "Details": pop_attr_list[3:]
        })
        dayschedule_contents.append(dayone)
        dayschedule_contents.append(daytwo)
    else:
        dayone.update({
            "Details": pop_attr_list[0:3]
        })
        daytwo.update({
            "Details": pop_attr_list[3:6]
        })
        dayschedule_contents.append(dayone)
        dayschedule_contents.append(daytwo)

    schedule_content.update({
        "dayScheduleContents": dayschedule_contents
    })
    target_schedule.update({
        "scheduleType": "EDITING",
        "scheduleContent": schedule_content
    })
    # print(target_schedule)
    update_schedule(target_schedule)
    return {
        'statusCode': 200,
        'body': json.dumps({
            "code": 200,
            "msg": "Submit successfully"
        })
    }


def submit_post_schedule(user_id, schedule_id, submit_detail):
    succ, response_schedule = get_target_schedule(schedule_id)
    if not succ:
        return response_schedule
    target_schedule = response_schedule["Item"]
    if target_schedule["scheduleType"].upper() != "PRESELECT":
        return {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "Can not submit schedule with non-PRESELECT type"
            })
        }
    if user_id != target_schedule["ownerId"]:
        return {
            'statusCode': 403,
            'body': json.dumps({
                "code": 403,
                "msg": "Permission Denied"
            })
        }

    mode_list = ["BUSY", "MEDIUM", "RELAX"]
    mode_dict = {
        "BUSY": 3,
        "MEDIUM": 2,
        "RELAX": 1
    }
    print("jiji1")
    print(submit_detail["mode"].upper())
    if submit_detail["mode"].upper() not in mode_list and submit_detail["model"] is None:
        print("jiji2")
        submit_schedule(user_id, schedule_id)
    view_mode = submit_detail["mode"].upper()
    print("jiji23")
    print(view_mode)
    num_attr_oneday = mode_dict[view_mode]
    print(num_attr_oneday)
    print("jiji3")
    try:
        num_day = int(submit_detail["day"])
        if num_day >= 7:
            return {
                'statusCode': 403,
                'body': json.dumps({
                    "code": 403,
                    "msg": "Days error"
                })
            }
    except Exception as e:
        return False, {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": str(e)
            })
        }

    schedule_content = {
        "metaData": "dummy"
    }
    dayschedule_contents = [{"NumDate": "day" + str(i + 1)} for i in range(num_day)]

    preselect_attr_list = list(target_schedule["scheduleContent"].keys())
    preselect_attr_first = str(preselect_attr_list[0])
    response_list = attraction_table.scan(ProjectionExpression="attractionId,score")
    attr_score_item_list = response_list["Items"]
    attr_score_item_list.sort(key=lambda a: -a["score"])
    pop_attr_list_db = list(map(lambda a: str(a["attractionId"]), attr_score_item_list))
    pop_attr_list_db.insert(0, preselect_attr_first)
    pop_attr_list = list(dict.fromkeys(pop_attr_list_db))
    print("jiji4")
    try:
        start_day = 0
        for i in range(num_day):
            dayschedule_contents[i].update({
                "Details": pop_attr_list[start_day:start_day + num_attr_oneday]
            })
            start_day = start_day + num_attr_oneday
    except Exception as e:
        return False, {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "Attractions are not enough"
            })
        }
    schedule_content.update({
        "dayScheduleContents": dayschedule_contents
    })
    target_schedule.update({
        "scheduleType": "EDITING",
        "scheduleContent": schedule_content
    })
    # print(target_schedule)
    update_schedule(target_schedule)
    return {
        'statusCode': 200,
        'body': json.dumps({
            "code": 200,
            "msg": "Submit successfully"
        })
    }


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
            response.update(submit_schedule(user_id, schedule_id))
        elif event["httpMethod"].upper() == "POST":
            response.update(submit_post_schedule(user_id, schedule_id, json.loads(event["body"])))
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
