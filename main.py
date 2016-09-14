# -*- coding: utf-8 -*-

import config.config3 as config
import src.object_manager as om
import src.watchdog_impl as wd
import src.oss2_utils as util
import logging.config
import time
import oss2.utils
from watchdog.observers import Observer

# logging config
logging.config.fileConfig(r"log\config")
logger = logging.getLogger("main")

# oss config
auth = oss2.Auth(config.auth_key, config.auth_key_secret)
bucket = oss2.Bucket(auth, config.endpoint, config.bucket_name)
service = oss2.Service(auth, config.endpoint, connect_timeout=config.connect_timeout)
object_manager = om.ObjectManager(bucket)

################################# test ###########################################
# md5 = util.file_md5("testPayLoad.html")
# result = object_manager.put_object("test/testPayLoad.html", "testPayLoad.html")
# result = object_manager.get_object("test/testPayLoad.html", "testPayLoad.html")
#
# a = 2

observers = []
for local_root in config.directory_mapping.keys():
    try:
        observer = Observer()
        event_handler = wd.FileEventHandler(bucket)
        observer.schedule(event_handler, local_root, True)  # 开启递归，文件夹的变动会依次触发子项的变动
        observer.start()
        observers.append(observer)
    except Exception as e:
        logger.error("observer-init error-- " + util.exception_string(e))

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    [observer.stop() for observer in observers]
[observer.join() for observer in observers]
##################################################################################