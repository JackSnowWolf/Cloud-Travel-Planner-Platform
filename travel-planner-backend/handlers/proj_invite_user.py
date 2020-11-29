import json
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

sqsClient = boto3.resource('sqs')
queue = sqsClient.get_queue_by_name(QueueName='travel-invitation-mq')


def send_to_sqs(owner_user_id, invited_user_id, schedule_id):
    inviteQuery = {
        "ownerUserId": owner_user_id,
        "invitedUserId": invited_user_id,
        "scheduleId": schedule_id
    }
    try:
        response = queue.send_message(MessageBody=json.dumps(inviteQuery))
        logger.info('response={}'.format(json.dumps(response)))
    except Exception as e:
        logger.error(e)
        return {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "put into message queue error"
            })
        }


def lambda_handler(event, context):
    # TODO implement
    try:
        owner_user_id = event["pathParameters"]["userId"]
        invited_user_id = event["queryStringParameters"]["userId"]
        schedule_id = event["queryStringParameters"]["scheduleId"]
        send_to_sqs(owner_user_id, invited_user_id, schedule_id)
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "missing required parameters!"
            })
        }
    logger.info("event={}".format(json.dumps(event)))
    return {
        'statusCode': 200,
        'body': json.dumps({
            "code": 200,
            "msg": "send invitation successfully"
        })
    }
