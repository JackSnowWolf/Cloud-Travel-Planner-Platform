import json
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

q_name = "travel-invitation-mq"
user_table = boto3.resource('dynamodb').Table('userTable')
sender_email="cchenwenjie0901@gmail.com"
authUrl="http://localhost:8080/#/accept/schedule/"

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


def pollSQS():
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=q_name)
    response = queue.receive_messages(MaxNumberOfMessages=1)
    if len(response) == 0:
        logger.info("no message")
        return "no message in the queue."

    return response


def sendSMS(owner_user_name, invited_user_id, invited_user_email, schedule_id):
    subject="Your invitation to a schedule."
    charset="UTF-8"

    msg_text = "Dear guest! \nYour friend %s send you an invitation.\n" % owner_user_name
    msg_text += "The schedule id for you to view is: %s\n\n" % schedule_id
    msg_text += "Please click here to accept the invitation:\n" + authUrl+schedule_id+"?editorId="+invited_user_id
    logger.debug("SMS message:\n" + msg_text)

    client=boto3.client('ses',region_name="us-east-1")
    response = client.send_email(
        Destination={
            'ToAddresses': [
                invited_user_email,
            ],
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': charset,
                    'Data': msg_text,
                },
            },
            'Subject': {
                'Charset': charset,
                'Data': subject,
            },
        },
        Source=sender_email
    )

    return {"statusCode": 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT",
                "Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
            },
            'body': "add visitor info and send SMS succefully!",
            }


def lambda_handler(event, context):
    logger.debug(json.dumps(event, indent=2))

    SQS_response = pollSQS()

    for SQS_r in SQS_response:
        r_data = json.loads(SQS_r.body)
        logger.debug("sending data: " + json.dumps(r_data))

        owner_user_id = r_data["ownerUserId"]
        invited_user_id = r_data["invitedUserId"]
        schedule_id = r_data["scheduleId"]

        succ1, response_invited = get_target_user(invited_user_id)
        if not succ1:
            return response_invited
        invited_user_email = response_invited["Item"]["userEmail"]

        succ2, response_owner = get_target_user(owner_user_id)
        if not succ2:
            return response_owner
        owner_user_name = response_owner["Item"]["userName"]

        logger.debug("sending data to email: " + invited_user_email)
        # owner_user_email = response_owner["Item"]["userEmail"]

        sendSMS(owner_user_name, invited_user_id, invited_user_email, schedule_id)


    return {
        'statusCode': 200,
        'body': json.dumps({
            "code": 200,
            "msg": "send email successfully"
        })
    }
