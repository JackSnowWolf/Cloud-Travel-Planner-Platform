import json
import logging
import sys
import unittest

from handlers.proj_send_invitation import lambda_handler
from handlers.proj_send_invitation import logger

logging.basicConfig(format='%(asctime)s %(filename)s [line:%(lineno)d] [PID:%(process)d] %(levelname)s: %(message)s',
                    stream=sys.stdout)


class SendInvitationCase(unittest.TestCase):
    def test_send_email(self):
        logger.info("test send")
        send_event={

        }
        handler_response = lambda_handler(send_event, None)
        logger.debug(json.dumps(handler_response, indent=2))
        logger.debug(json.dumps(json.loads(handler_response["body"]), indent=2))
        self.assertEqual(handler_response["statusCode"], 200)
        logger.info("Completed!")


if __name__ == '__main__':
    unittest.main()
