# -*- coding: utf-8 -*-

import config.config as config
import src.object_manager as om
import logging
import logging.config
import oss2

# logging config
logging.config.fileConfig(r"log\config")
logger = logging.getLogger("main")

# oss config
auth = oss2.Auth(config.auth_key, config.auth_key_secret)
bucket = oss2.Bucket(auth, config.endpoint, config.bucket_name)
service = oss2.Service(auth, config.endpoint, connect_timeout=config.connect_timeout)

result = om.put_file(bucket, "test/testPayLoad.html", "testPayLoad.html")
# result = om.get_file(bucket, "testPayLoad.html", "test/testPayLoad.html")
# result = bucket.head_object("test/testPayLoad.html")

a = 2