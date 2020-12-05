import json
import logging
import sys
import unittest

from handlers.proj_schedule_attraction_selector import lambda_handler
from handlers.proj_schedule_attraction_selector import logger
from handlers.proj_schedule_attraction_selector import update_schedule

logging.basicConfig(format='%(asctime)s %(filename)s [line:%(lineno)d] [PID:%(process)d] %(levelname)s: %(message)s',
                    stream=sys.stdout)


class ScheduleAttractionSelectorTestCase(unittest.TestCase):
    def test_get_schedule_attraction_selector(self):
        logger.info("test get schedule handler")
        update_schedule({
            "targetArea": "New York",
            "scheduleId": "preselect-schedule-example-for-selector",
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
            "resource": "/schedule/{scheduleId}/attraction/{attractionId}",
            "path": "/schedule/preselect-schedule-example-for-selector/attraction/attr-0001",
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
                "scheduleId": "preselect-schedule-example-for-selector",
                "attractionId": "attr-0001"
            }
        }
        handler_response = lambda_handler(get_test_event, None)
        logger.debug(json.dumps(handler_response, indent=2))
        logger.debug(json.dumps(json.loads(handler_response["body"]), indent=2))
        self.assertEqual(handler_response["statusCode"], 200)
        logger.info("Completed!")

    def test_put_schedule_attraction_selector(self):
        self.assertEqual(True, False)

    def test_post_schedule_attraction_selector(self):
        self.assertEqual(True, False)

    def test_delete_schedule_attraction_selector(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
