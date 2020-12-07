import datetime
import json
import os
import uuid
from optparse import OptionParser

from utils.upload.config import config
from utils.upload.upload_data_to_dynamodb import upload_data_to_dynamodb
from utils.upload.upload_data_to_es import upload_data_to_es
from utils.upload.upload_sitephoto_to_s3 import upload_file_to_s3


def init_parser():
    parser = OptionParser()
    parser.add_option("--aws-s3-img-bucket-name", action="store",
                      dest="AWS_S3_IMG_BUCKET_NAME",
                      default=None,
                      help="set s3 image bucket")
    options, _ = parser.parse_args()
    if options.AWS_S3_IMG_BUCKET_NAME is not None:
        config.set("aws", "AWS_S3_IMG_BUCKET_NAME", str(options.AWS_S3_IMG_BUCKET_NAME))
    return


def extract_json(complete_file_path):
    input_file = open(os.path.normpath(complete_file_path), 'rb')
    json_decode = json.load(input_file)
    return json_decode


def upload_single_data(json_data):
    attraction_id = "attr-" + str(uuid.uuid1())
    attraction_name = json_data['attractionName']
    attraction_description = json_data['attractionDescription']
    attraction_loc = json_data['attractionLoc']
    attraction_type = json_data['attractionType']
    attraction_area = json_data["attractionArea"]
    score = json_data['score']
    estimate_view_time = json_data['estimateViewTime']
    time = str(datetime.datetime.now())
    attraction_imgs = list(map(lambda x: {
        "bucket": config["aws"]["AWS_S3_IMG_BUCKET_NAME"],
        "createdTimestamp": time,
        "objectKey": x
    }, json_data['imgsName']))

    attraction_labels = json_data['labels']

    # upload to db
    upload_data_to_dynamodb(attraction_id,
                            attraction_name,
                            attraction_description,
                            attraction_area,
                            attraction_loc,
                            attraction_type,
                            score,
                            estimate_view_time,
                            attraction_imgs)

    # upload to es
    upload_data_to_es(attraction_id, attraction_name, attraction_type, attraction_area, time, attraction_labels)

    # upload to
    complete_file_path = config["data"]["DATA_IMG_FOLDER"] + json_data['imgsName'][0]
    upload_file_to_s3(complete_file_path, json_data['imgsName'][0])
    complete_file_path = config["data"]["DATA_IMG_FOLDER"] + json_data['imgsName'][1]
    upload_file_to_s3(complete_file_path, json_data['imgsName'][1])


def upload_all():
    print(os.path.normpath("."))

    for json_data_file_name in os.listdir(config["data"]["DATA_JSON_FOLDER"]):
        json_data_file_path = os.path.join(config["data"]["DATA_JSON_FOLDER"], json_data_file_name)
        json_data = extract_json(json_data_file_path)
        upload_single_data(json_data)


if __name__ == '__main__':
    upload_all()
