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
                    {
                        "NumDate": "day1",
                        "Details": [
                            "attr-11111111-308c-11eb-9017-54e1ad16ceb2",
                            "attr-19f83044-36f6-11eb-875e-a683e780ed71"
                        ]
                    }
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
                "scheduleId": "editing-schedule-03"
            },
            "body": json.dumps({
                    "metaData": "dummy",
                    "dayScheduleContents": [
                        {
                            "NumDate": "day1",
                            "Details": [
                                "attr-ca428d3e-308c-11eb-9017-54e1ad16ceb2",
                                "attr-2f6c194e-3094-11eb-9017-54e1ad16ceb2"
                            ]
                        },
                        {
                            "NumDate": "day2",
                            "Details": [
                                "attr-3f6c194e-3094-11eb-9017-54e1ad16ceb2"
                            ]
                        }
                    ]
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
                    {
                        "NumDate": "day1",
                        "Details": [
                            "attr-ca428d3e-308c-11eb-9017-54e1ad16ceb2",
                            "attr-2f6c194e-3094-11eb-9017-54e1ad16ceb2"
                        ]
                    },
                    {
                        "NumDate": "day2",
                        "Details": [
                            "attr-3f6c194e-3094-11eb-9017-54e1ad16ceb2"
                        ]
                    }
                ]
            },
            "scheduleType": "COMPLETE",
            "editorIds": [],
            "ownerId": "test-owner",
            "scheduleTitle": "Example Schedule"
        }
        )
        from handlers.proj_schedule_initializer import update_user_info_editable_schedules
        update_user_info_editable_schedules(
            {"userId": "test-owner", "editableSchedules": ["test-delete-schedule-sample"]})

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
