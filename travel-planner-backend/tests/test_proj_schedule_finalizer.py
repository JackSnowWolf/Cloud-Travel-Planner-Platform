import json
import logging
import sys
import unittest

from handlers.proj_schedule_finalizer import lambda_handler
from handlers.proj_schedule_finalizer import logger

logging.basicConfig(format='%(asctime)s %(filename)s [line:%(lineno)d] [PID:%(process)d] %(levelname)s: %(message)s',
                    stream=sys.stdout)


class ScheduleFinalizerTestCase(unittest.TestCase):
    def test_get_schedule_finalizer(self):
        logger.info("test get schedule finalizer")

        from handlers.proj_schedule_finalizer import update_schedule

        update_schedule({
            "targetArea": "New York",
            "scheduleId": "test-finalized-schedule-sample",
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
                            "attr-ba428d3e-308c-11eb-9017-54e1ad16ceb2",
                            "attr-3f6c194e-3094-11eb-9017-54e1ad16ceb2"
                        ]
                    }
                ]
            },
            "scheduleType": "EDITING",
            "editorIds": [
                "test-editor"
            ],
            "ownerId": "test-owner",
            "scheduleTitle": "Example Schedule"
        }
        )

        get_test_event = {
            "resource": "/schedule/{scheduleId}/finish",
            "path": "/attraction/test-finalized-schedule-sample/finish",
            "httpMethod": "GET",
            "queryStringParameters": {
                "userId": "test-owner"
            },
            "multiValueQueryStringParameters": {
                "userId": [
                    "test-owner"
                ]
            },
            "pathParameters": {
                "scheduleId": "test-finalized-schedule-sample"
            }
        }

        handler_response = lambda_handler(get_test_event, None)
        logger.debug(json.dumps(handler_response, indent=2))
        logger.debug(json.dumps(json.loads(handler_response["body"]), indent=2))
        self.assertEqual(handler_response["statusCode"], 200)
        logger.info("Completed!")


if __name__ == '__main__':
    unittest.main()
