import json
import logging
import sys
import unittest

from handlers.proj_schedule_submitter import lambda_handler
from handlers.proj_schedule_submitter import logger

logging.basicConfig(format='%(asctime)s %(filename)s [line:%(lineno)d] [PID:%(process)d] %(levelname)s: %(message)s',
                    stream=sys.stdout)


class ScheduleSubmitterCase(unittest.TestCase):
    def test_get_schedule_submitter(self):
        logger.info("test get schedule submitter")
        get_test_event = {
            "resource": "/schedule/{scheduleId}/submit",
            "path": "/attraction/test-submit-schedule-sample/submit",
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
                "scheduleId": "preselect-schedule-example-for-submit4"
            }
        }
        handler_response = lambda_handler(get_test_event, None)
        logger.debug(json.dumps(handler_response, indent=2))
        logger.debug(json.dumps(json.loads(handler_response["body"]), indent=2))
        self.assertEqual(handler_response["statusCode"], 200)
        logger.info("Completed!")


if __name__ == '__main__':
    unittest.main()
