import json

import requests

from .config import config
from .config import logger

AWS_ES_ENDPOINT = config["aws"]["AWS_ES_ENDPOINT"]

AWS_ES_SUBDOMAIN = config["aws"]["AWS_ES_SUBDOMAIN"]


def upload_data_to_es(
        object_key,
        attraction_name,
        attraction_type,
        attraction_area,
        time,
        labels):
    """
    Uploads data to es.
    """
    url = "{:s}/{:s}/_doc".format(AWS_ES_ENDPOINT, AWS_ES_ENDPOINT)

    header = {"Content-Type": "application/json"}

    params = {
        "objectKey": object_key,
        "attractionName": attraction_name,
        "attractionType": attraction_type,
        "attractionArea": attraction_area,
        "createdTimestamp": time,
        "labels": labels
    }

    response_es = requests.post(url, data=json.dumps(params), headers=header)
    logger.info("response data:" + json.dumps(response_es.json()))

