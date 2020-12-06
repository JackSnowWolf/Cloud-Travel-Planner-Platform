import configparser
import logging
import os
import sys

logging.basicConfig(format='%(asctime)s %(filename)s [line:%(lineno)d] [PID:%(process)d] %(levelname)s: %(message)s',
                    stream=sys.stdout)

config = configparser.ConfigParser()
config.read("upload.config")
config.read(os.path.join("upload", "upload.config"))

logger = logging.getLogger()
logger.setLevel(config["logger"]["LEVEL"])
