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

import src.oss2_utils as util
import logging
import time
import os

logger_main = logging.getLogger("main_logger")
logger_err = logging.getLogger('err_logger')


class OssObject(object):
    """
    oss object model for a local file or directory
    """

    # since bucket.put_object() may get 407 when content is empty,
    # I give all directory objects "$DIRECTORY$" as content
    DIR_CONTENT = "$DIRECTORY$"

    # MD5 of DIR_CONTENT, local folders will get this MD5 as etag
    DIR_MD5 = '48f3ac15a4a8540d13a1b883b8d3ee73'

    def __init__(self, local_path):
        """
        :param local_path:
        """
        if not os.path.exists(local_path):
            raise FileNotFoundError
        self.__loc_path = local_path
        self.__is_dir = os.path.isdir(local_path)
        self.__etag = OssObject.DIR_MD5 if self.__is_dir else util.file_md5(local_path)
        self.__lmt = time.mktime(time.gmtime()) if self.__is_dir else os.path.getmtime(local_path)

    @property
    def key(self):
        return self.__loc_path

    @property
    def etag(self):
        return self.__etag

    @property
    def last_modified(self):
        return self.__lmt

    @property
    def is_prefix(self):
        return self.__is_dir

    @property
    def size(self):
        return os.path.getsize(self.__loc_path)
