import json
import logging
import sys
import unittest

from handlers.proj_accept_invitation import lambda_handler
from handlers.proj_accept_invitation import logger

logging.basicConfig(format='%(asctime)s %(filename)s [line:%(lineno)d] [PID:%(process)d] %(levelname)s: %(message)s',
                    stream=sys.stdout)


class InvitationAcceptCase(unittest.TestCase):
    def test_accept_invitation(self):
        logger.info("test accept invitation")
        get_test_event = {
            "resource": "/accept/{scheduleId}",
            "path": "/accept/editing-schedule",
            "httpMethod": "GET",
            "queryStringParameters": {
                "editorId": "user-1f402a34-567f-4f88-a489-7be3528ae019"
            },
            "multiValueQueryStringParameters": {
                "editorId": [
                    "user-1f402a34-567f-4f88-a489-7be3528ae019"
                ]
            },
            "pathParameters": {
                "scheduleId": "sche-0edbb4b6-44dd-11eb-ad31-620febc79dc7"
            },
        }
        handler_response = lambda_handler(get_test_event, None)
        logger.debug(json.dumps(handler_response, indent=2))
        logger.debug(json.dumps(json.loads(handler_response["body"]), indent=2))
        self.assertEqual(handler_response["statusCode"], 200)
        logger.info("Completed!")


if __name__ == '__main__':
    unittest.main()
