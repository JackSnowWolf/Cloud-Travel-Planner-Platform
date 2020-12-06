import json
import logging
import sys
import unittest

from handlers.proj_attraction_searcher import lambda_handler
from handlers.proj_attraction_searcher import logger

logging.basicConfig(format='%(asctime)s %(filename)s [line:%(lineno)d] [PID:%(process)d] %(levelname)s: %(message)s',
                    stream=sys.stdout)


class AttractionSearcherCase(unittest.TestCase):
    def test_get_attraction_searcher(self):
        logger.info("test get attraction searcher")
        get_test_event = {
            "resource": "/attraction/_search",
            "path": "attraction/_search",
            "httpMethod": "GET",
            "queryStringParameters": {
                "q": "NewYork"
            },
            "multiValueQueryStringParameters": {
                "q": [
                    "NewYork"
                ]
            },
            "pathParameters": {
            }
        }
        handler_response = lambda_handler(get_test_event, None)
        logger.debug(json.dumps(handler_response, indent=2))
        logger.debug(json.dumps(json.loads(handler_response["body"]), indent=2))
        self.assertEqual(handler_response["statusCode"], 200)
        logger.info("Completed!")


if __name__ == '__main__':
    unittest.main()
