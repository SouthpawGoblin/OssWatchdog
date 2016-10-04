# -*- coding: utf-8 -*-

# Copyright 2016 Qi Yinzhe(Yinzhe-Qi) <goblin-qyz@163.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import config.config as config
import src.watchdog_impl as wd
import src.oss2_utils as util
import src.object_manager as om
import logging.config
import time
import oss2.utils
from watchdog.observers import Observer

mapping = config.directory_mapping

# logging config
logging.config.fileConfig(r"log\config")
logger = logging.getLogger("main")

# oss config
auth = oss2.Auth(config.auth_key, config.auth_key_secret)
service = oss2.Service(auth, config.endpoint, connect_timeout=config.connect_timeout)

# TODO: on init, check config.directory_mapping for duplicate values
# TODO: on init, check local time and server time, give warning if the two differs 15mins plus

################################# test ###########################################
# md5 = util.file_md5("testPayLoad.html")
# print(md5)
# result = object_manager.put_object("test/testPayLoad.html", "testPayLoad.html")
# result = object_manager.get_object("test/testPayLoad.html", "testPayLoad.html")
#
# a = 2

observers = []
for local_root, remote_root in mapping.items():
    try:
        observer = Observer()
        bucket = oss2.Bucket(auth, config.endpoint, remote_root[0])
        event_handler = wd.FileEventHandler(bucket, (local_root, remote_root[1]))
        observer.schedule(event_handler, local_root, True)
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