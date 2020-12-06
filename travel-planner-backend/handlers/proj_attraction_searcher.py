import json
import logging
import urllib
from decimal import Decimal

import boto3
import requests

# from botocore.vendored import requests

ELASTICSEARCH_BASE_URL = "https://search-proj-for-attractions-um6r2mitevcydyzporkglj72ea.us-east-1.es.amazonaws.com"
ATTRACTION_ELASTICSEARCH_URL = "{:s}/{:s}/_search".format(ELASTICSEARCH_BASE_URL, "attractions")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

attraction_table = boto3.resource('dynamodb').Table('attractionTable')


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


def extract_item(item):
    bucket = item["bucket"]
    object_key = item["objectKey"]
    return "https://{:s}.s3.amazonaws.com/{:s}".format(bucket, object_key)


def extract_attraction(attraction_info):
    attraction_img_urls = list(map(extract_item, attraction_info["attractionImgs"]))
    del attraction_info["attractionImgs"]
    attraction_info["attractionImgUrls"] = attraction_img_urls
    return attraction_info


def search_attractions_on_es(query, page_size=10, page_no=0):
    try:
        url = ATTRACTION_ELASTICSEARCH_URL
        params = {
            "q": query,
            "from": page_no * page_size,
            "size": page_size
        }
        params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        es_response = requests.get(url, params=params).json()

        logger.debug(json.dumps(es_response, indent=2))
        if "hits" not in es_response and "hits" not in es_response["hits"]:
            return False, None, {
                'statusCode': 400,
                'body': "Elasticsearch can not get results"
            }
        return True, es_response["hits"]["total"]["value"], es_response["hits"]["hits"]
    except Exception as e:
        logger.error(str(e))
        return False, None, {
            'statusCode': 400,
            'body': "Elasticsearch can not get results"
        }


def batch_get_attraction(attraction_id_list):
    try:
        response = boto3.resource('dynamodb').batch_get_item(
            RequestItems={
                "attractionTable": {
                    "Keys": list(map(lambda attraction_id: {"attractionId": attraction_id}, attraction_id_list)),
                }
            }
        )

        if "Responses" in response and len(response["UnprocessedKeys"]) == 0:
            return True, response["Responses"]
        return False, {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "can not get attraction attributes"
            })
        }
    except Exception as e:
        logger.error(e)
        return False, {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "attraction id doesn't exist"
            })
        }


def search_attractions(query, page_size=10, page_no=0):
    succ, total, response = search_attractions_on_es(query, page_size, page_no)
    if not succ:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "Cannot search on elasticsearch"
            })
        }
    attraction_list = response
    attraction_id_list = list(map(lambda x: x["_source"]["objectKey"], attraction_list))
    succ, response = batch_get_attraction(set(attraction_id_list))
    if not succ:
        return response
    attraction_info_list = response["attractionTable"]
    attraction_info_list_response = list(map(extract_attraction, attraction_info_list))
    return {
        'statusCode': 200,
        'body': json.dumps({"total": total,
                            "data": attraction_info_list_response},
                           cls=DecimalEncoder)
    }


def lambda_handler(event, context):
    response = {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE,PATCH",
            "Access-Control-Allow-Headers": "Content-Type,Access-Control-Allow-Headers, Authorization, X-Requested-With"
        }
    }
    try:
        logger.info("event={}".format(json.dumps(event)))
        if "q" not in event["queryStringParameters"]:
            query = "*:*"
        else:
            query = event["queryStringParameters"]["q"]

        if "pageSize" not in event["queryStringParameters"]:
            page_size = 20
        else:
            page_size = int(event["queryStringParameters"]["pageSize"])
        if "pageNo" not in event["queryStringParameters"]:
            page_no = 0
        else:
            page_no = int(event["queryStringParameters"]["pageNo"])
        if event["httpMethod"].upper() == "GET":
            response.update(search_attractions(query, page_size=page_size, page_no=page_no))
            return response
        response.update({
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "http method not supported"
            })
        })
    except Exception as e:
        logger.error(e)
        response.update({
            'statusCode': 400,
            'body': json.dumps({
                "code": 400,
                "msg": "Bad Requset!"
            })
        })
        return response
