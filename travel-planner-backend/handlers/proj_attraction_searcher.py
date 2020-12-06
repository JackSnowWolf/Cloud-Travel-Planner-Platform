import json
import logging
from decimal import Decimal

import boto3
from botocore.vendored import requests

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

attraction_table = boto3.resource('dynamodb').Table('attractionTable')


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


def search_attractions(query):
    pass

