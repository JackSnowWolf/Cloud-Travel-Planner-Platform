import json
import logging
import sys
import unittest

from handlers.proj_schedule_handler import lambda_handler
from handlers.proj_schedule_handler import logger
from handlers.proj_schedule_handler import update_schedule

logging.basicConfig(format='%(asctime)s %(filename)s [line:%(lineno)d] [PID:%(process)d] %(levelname)s: %(message)s',
                    stream=sys.stdout)


class ScheduleHandlerTestCase(unittest.TestCase):
    def test_get_schedule_handler_for_preselect_schedule(self):
        logger.info("test get preselect schedule handler")
        update_schedule({
            "targetArea": "New York",
            "scheduleId": "preselect-schedule",
            "revisedTimeStamp": "1606467266",
            "scheduleContent": {"attr-0001": {
                "isSelected": False,
                "selectedNumber": 0,
                "selectedUsers": []
            }},
            "scheduleType": "PRESELECT",
            "editorIds": [
                "test-editor"
            ],
            "ownerId": "test-owner",
            "scheduleTitle": "Example Schedule"
        })

        get_test_event = {
            "resource": "/schedule/{scheduleId}",
            "path": "/schedule/preselect-schedule",
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
                "scheduleId": "preselect-schedule"
            }
        }
        handler_response = lambda_handler(get_test_event, None)
        logger.debug(json.dumps(handler_response, indent=2))
        logger.debug(json.dumps(json.loads(handler_response["body"]), indent=2))
        self.assertEqual(handler_response["statusCode"], 200)
        logger.info("Completed!")

    def test_get_schedule_handler_for_editing_schedule(self):
        logger.info("test get schedule handler")
        update_schedule({
            "scheduleId": "editing-schedule-for-get-schedule-test",
            "scheduleTitle": "Example Schedule",
            "revisedTimeStamp": "1606467266",
            "targetArea": "New York",
            "ownerId": "test-owner",
            "editorIds": [
                "test-editor"
            ],
            "scheduleType": "EDITING",
            "scheduleContent": {
                "metaData": "dummy",
                "dayScheduleContents": [
                    [
                        "attr-0001"
                    ]
                ]
            }
        })
        get_test_event = {
            "resource": "/schedule/{scheduleId}",
            "path": "/schedule/editing-schedule-for-get-schedule-test",
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
                "scheduleId": "editing-schedule-for-get-schedule-test"
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
