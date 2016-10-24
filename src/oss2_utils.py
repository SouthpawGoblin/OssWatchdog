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

from hashlib import md5
import requests
import time
import oss2
import os
import logging

logger_main = logging.getLogger("main_logger")
logger_err = logging.getLogger('err_logger')


def get_server_time():
    """
    get server time (GMT timestamp)
    :return:
    """
    response = requests.get('http://www.aliyun.com')
    t = response.headers.get('date')
    time_tuple = time.strptime(t[5:25], "%d %b %Y %H:%M:%S")
    stamp = int(time.mktime(time_tuple))
    return stamp


def exception_string(e):
    """
    transfer OssError into string
    :param e:
    :return:
    """
    if e is oss2.exceptions.OssError:
        return "OssError: status= " + e.status + \
               "||request_id= " + e.request_id + \
               "||code= " + e.code + \
               "||message= " + e.message
    else:
        return str(e)


def file_md5(file):
    """
    calculation file md5 (upper case)
    :param file:
    :return:
    """
    m = md5()
    if os.path.isdir(file):
        m.update(file.encode())
    else:
        a_file = open(file, 'rb')  # 需要使用二进制格式读取文件内容
        m.update(a_file.read())
        a_file.close()
    return m.hexdigest().upper()


