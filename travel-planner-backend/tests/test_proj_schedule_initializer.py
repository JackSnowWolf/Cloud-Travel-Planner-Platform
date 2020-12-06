import json
import logging
import sys
import unittest

from handlers.proj_schedule_initializer import lambda_handler
from handlers.proj_schedule_initializer import logger

logging.basicConfig(format='%(asctime)s %(filename)s [line:%(lineno)d] [PID:%(process)d] %(levelname)s: %(message)s',
                    stream=sys.stdout)


class ScheduleInitializerTestCase(unittest.TestCase):

    def test_get_schedule_initializer(self):
        logger.info("test get schedule initializer")
        get_test_event = {
            "resource": "/schedule/",
            "path": "/schedule/",
            "httpMethod": "GET",
            "queryStringParameters": {
                "pageSize": "20",
                "pageNo": "0",
                "userId": "test-editor"
            },
            "multiValueQueryStringParameters": {
                "pageSize": [
                    "20"
                ],
                "pageNo": [
                    "0"
                ],
                "userId": [
                    "test-editor"
                ]
            },
            "pathParameters": {}
        }
        handler_response = lambda_handler(get_test_event, None)
        logger.debug(json.dumps(handler_response, indent=2))
        logger.debug(json.dumps(json.loads(handler_response["body"]), indent=2))
        self.assertEqual(handler_response["statusCode"], 200)
        logger.info("Completed!")

    def test_post_schedule_initializer(self):
        logger.info("test post schedule initializer")
        post_test_event = {
            "resource": "/schedule/",
            "path": "/schedule/",
            "httpMethod": "POST",
            "queryStringParameters": {
                "targetArea": "New York",
                "userId": "test-editor"
            },
            "multiValueQueryStringParameters": {
                "targetArea": [
                    "New York"
                ],
                "userId": [
                    "test-editor"
                ],
            },
            "pathParameters": {}
        }
        handler_response = lambda_handler(post_test_event, None)
        print(json.dumps(handler_response, indent=2))
        self.assertEqual(handler_response["statusCode"], 200)
        logger.debug(json.dumps(json.loads(handler_response["body"]), indent=2))
        logger.info("Completed!")


if __name__ == '__main__':
    unittest.main()
