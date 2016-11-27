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
import src.sync_socket as ss
import src.oss2_utils as util
import logging.config
import log.log_config as log_conf
import time
import oss2.utils
from watchdog.observers import Observer

# logging config
logging.config.dictConfig(log_conf.config)
logger_main = logging.getLogger("main_logger")
logger_err = logging.getLogger('err_logger')

# oss config
auth = oss2.Auth(config.auth_key, config.auth_key_secret)
service = oss2.Service(auth, config.endpoint, connect_timeout=config.connect_timeout)

# TODO: maintain a queue to record local file changes while synchronize() is running
# TODO: on init, check local time and server time, give warning if the two differs 15mins plus

################################# test ###########################################
# md5 = util.file_md5("testPayLoad.html")
# print(md5)
# result = object_manager.put_object("test/testPayLoad.html", "testPayLoad.html")
# result = object_manager.get_object("test/testPayLoad.html", "testPayLoad.html")
#
# a = 2

# check config.directory_mapping for duplicate values
if len(set(config.directory_mapping.keys())) < len(config.directory_mapping):
    logger_err.error("init error | duplicate local paths found in directory mapping")
if len(set([v[1] for v in config.directory_mapping.values()])) < len(config.directory_mapping):
    logger_err.error("init error | duplicate remote paths found in directory mapping")

# normalize config paths
mapping = {}
for item in config.directory_mapping.items():
    local = util.local_path_norm(item[0])
    bkt = item[1][0]
    remote = util.remote_path_norm(item[1][1])
    mapping[local] = (bkt, remote)
config.directory_mapping = mapping

# initialize watchdog observers
observers = []
for local_root, remote_root in mapping.items():
    try:
        observer = Observer()
        bucket = oss2.Bucket(auth, config.endpoint, remote_root[0])
        sync_socket = ss.SyncSocket(bucket, (local_root, remote_root[1]))
        observer.schedule(sync_socket, local_root, True)
        observer.start()
        observers.append(observer)
        sync_socket.synchronize()
    except Exception as e:
        logger_err.error("observer-init error | " + util.exception_string(e))
        exit(1)
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    [observer.stop() for observer in observers]
[observer.join() for observer in observers]
##################################################################################