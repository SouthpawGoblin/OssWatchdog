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
import oss2
import os


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
    a_file = open(file, 'rb')  # 需要使用二进制格式读取文件内容
    m.update(a_file.read())
    a_file.close()
    return m.hexdigest().upper()


def local_to_remote(local, local_remote_root):
    """
    transfer local path to the corresponding remote path using directory map
    :param local:
    :param local_remote_root:
    :return:
    """
    assert local_remote_root[0] in local, 'local does not match local_root'
    rootl, rootr = local_remote_root[0], local_remote_root[1]
    common = local.split(rootl)[1]
    remote = rootr + common
    if len(os.path.splitext(remote)[-1]) == 0:
        remote += '/'
    remote = remote.replace('\\', '/')
    return remote


def remote_to_local(remote, local_remote_root):
    """
    transfer remote path to the corresponding local path using directory map
    :param remote:
    :param local_remote_root:
    :return:
    """
    assert local_remote_root[1] in remote, 'remote does not match remote_root'
    rootl, rootr = local_remote_root[0], local_remote_root[1]
    common = remote.split(rootr)[1]
    local = rootl + common
    local = local.replace('/', '\\')
    return local

