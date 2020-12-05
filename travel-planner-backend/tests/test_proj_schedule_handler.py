import json
import logging
import sys
import unittest

from handlers.proj_schedule_handler import lambda_handler
from handlers.proj_schedule_handler import logger

logging.basicConfig(format='%(asctime)s %(filename)s [line:%(lineno)d] [PID:%(process)d] %(levelname)s: %(message)s',
                    stream=sys.stdout)


class ScheduleHandlerTestCase(unittest.TestCase):
    def test_get_schedule_handler(self):
        logger.info("test get schedule handler")
        get_test_event = {
            "resource": "/schedule/{scheduleId}",
            "path": "/schedule/editing-schedule",
            "httpMethod": "GET",
            "queryStringParameters": {
                "userId": "test-editor"
            },
            "multiValueQueryStringParameters": {
                "userId": [
                    "test-editor"
                ]
            },
            "pathParameters": {
                "scheduleId": "editing-schedule"
            }
        }
        handler_response = lambda_handler(get_test_event, None)
        logger.debug(json.dumps(handler_response, indent=2))
        logger.debug(json.dumps(json.loads(handler_response["body"]), indent=2))
        self.assertEqual(handler_response["statusCode"], 200)
        logger.info("Completed!")

    def test_post_schedule_handler(self):
        logger.info("test post schedule handler")
        post_test_event = {
            "resource": "/schedule/{scheduleId}",
            "path": "/schedule/editing-schedule",
            "httpMethod": "POST",
            "queryStringParameters": {
                "userId": "test-editor"
            },
            "multiValueQueryStringParameters": {
                "userId": [
                    "test-editor"
                ]
            },
            "pathParameters": {
                "scheduleId": "editing-schedule"
            },
            "body": json.dumps({
                "targetArea": "New York",
                "scheduleId": "editing-schedule",
                "revisedTimeStamp": "1606467266",
                "scheduleContent": {
                    "metaData": "dummy",
                    "dayScheduleContents": [
                        [
                            "attr-ca428d3e-308c-11eb-9017-54e1ad16ceb2",
                            "attr-ca428d3e-308c-11eb-9017-54e1ad16ceb2"
                        ],
                        ["attr-ca428d3e-308c-11eb-9017-54e1ad16ceb2"]
                    ]
                },
                "scheduleType": "EDITING",
                "editorIds": [
                    "test-editor"
                ],
                "ownerId": "user-fafaaae8-308b-11eb-9017-54e1ad16ceb2",
                "scheduleTitle": "Example Schedule"
            }
            )

        }
        handler_response = lambda_handler(post_test_event, None)
        logger.debug(json.dumps(handler_response, indent=2))
        logger.debug(json.dumps(json.loads(handler_response["body"]), indent=2))
        self.assertEqual(handler_response["statusCode"], 200)
        logger.info("Completed!")

    def test_delete_schedule_handler(self):
        logger.info("test delete schedule handler")

        from handlers.proj_schedule_handler import update_schedule

        update_schedule({
            "targetArea": "New York",
            "scheduleId": "test-delete-schedule-sample",
            "revisedTimeStamp": "1606467266",
            "scheduleContent": {
                "metaData": "dummy",
                "dayScheduleContents": [
                    [
                        "attr-ca428d3e-308c-11eb-9017-54e1ad16ceb2",
                        "attr-ca428d3e-308c-11eb-9017-54e1ad16ceb2"
                    ],
                    ["attr-ca428d3e-308c-11eb-9017-54e1ad16ceb2"]
                ]
            },
            "scheduleType": "COMPLETE",
            "editorIds": [
                "test-editor"
            ],
            "ownerId": "test-owner",
            "scheduleTitle": "Example Schedule"
        }
        )

        delete_test_event = {
            "resource": "/schedule/{scheduleId}",
            "path": "/schedule/test-delete-schedule-sample",
            "httpMethod": "DELETE",
            "queryStringParameters": {
                "userId": "test-owner"
            },
            "multiValueQueryStringParameters": {
                "userId": [
                    "test-owner"
                ]
            },
            "pathParameters": {
                "scheduleId": "test-delete-schedule-sample"
            },
            "body": "{}"
        }
        handler_response = lambda_handler(delete_test_event, None)
        logger.debug(json.dumps(handler_response, indent=2))
        logger.debug(json.dumps(json.loads(handler_response["body"]), indent=2))
        self.assertEqual(handler_response["statusCode"], 200)
        logger.info("Completed!")


if __name__ == '__main__':
    unittest.main()
