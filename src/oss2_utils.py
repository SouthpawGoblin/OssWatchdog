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

# md5 of ""
NULL_MD5 = 'D41D8CD98F00B204E9800998ECF8427E'


# class ObjectNode(object):
#     """
#     deprecated, using OssObject instead
#     object tree node, representing the file structure
#     """
#     def __init__(self, relative_path=None, etag=None, last_modified_time=None):
#         """
#         :param relative_path: relative path name without local or remote root
#         :param etag:
#         :param last_modified_time:
#         """
#         self.__rem_path = relative_path
#         self.__etag = etag
#         self.__lmt = last_modified_time
#         self.__father = None
#         self.__children = set([])
#
#     def __eq__(self, other):
#         if not other.__rem_path or other.__rem_path != self.__rem_path:
#             return False
#         if not other.__etag or other.__etag != self.__etag:
#             return False
#         if not other.__lmt or other.__lmt != self.__lmt:
#             return False
#         if other.__children != self.__children:
#             return False
#         return True
#
#     @property
#     def relative_path(self):
#         return self.__rem_path
#
#     @property
#     def etag(self):
#         return self.__etag
#
#     @property
#     def last_modified_time(self):
#         return self.__lmt
#
#     def _update(self):
#         """
#         update lmt and etag all the way up to the root
#         :return:
#         """
#         current = self.__father
#         new_md5_int = int(self.__etag, 16)
#         while current:
#             current.__lmt = self.__lmt
#             old_md5_int = int(current.__etag, 16)
#             current.__etag = str(hex(old_md5_int ^ new_md5_int))[2:].upper()
#             new_md5_int = int(current.__etag, 16) ^ old_md5_int
#             current = current.__father
#
#     def is_dir(self):
#         """
#         :return:
#         """
#         return len(os.path.splitext(self.__rem_path)[-1]) == 0
#
#     def add_child(self, node):
#         """
#         :param node:
#         :return:
#         """
#         if node.__rem_path and node.__etag and node.__lmt:
#             node.__father = self
#             self.__children.add(node)
#             node._update()
#
#     def del_child(self, node):
#         """
#         :param node:
#         :return:
#         """
#         if node in self.__children:
#             node._update()
#             node.__father = None
#             self.__children.remove(node)

class OssObject(object):
    """
    oss object model for a local file
    """

    def __init__(self, remote_path=None, etag=None, last_modified_time=None):
        """
        :param remote_path: corresponding remote path name
        :param etag:
        :param last_modified_time:
        """
        self.__rem_path = remote_path
        self.__etag = etag
        self.__lmt = last_modified_time

    def __eq__(self, other):
        if not other:
            return False
        if not other.__rem_path or other.__rem_path != self.__rem_path:
            return False
        if not other.__etag or other.__etag != self.__etag:
            return False
        if not other.__lmt or other.__lmt != self.__lmt:
            return False
        return True

    @property
    def remote_path(self):
        return self.__rem_path

    @property
    def etag(self):
        return self.__etag

    @property
    def last_modified_time(self):
        return self.__lmt


def local_indexing(local_path, root_prefix):
    """
    generate local file index map {local_path: OssObject}
    :param local_path:
    :param root_prefix:
    :return:
    """
    if root_prefix not in local_path:
        raise Exception("local_path doesn't contains the specified root_prefix")
    oss_map = _recursive_indexing(local_path, None)
    return oss_map


def _recursive_indexing(local_path, oss_map):
    if not oss_map:
        oss_map = {}
    for _dir in os.listdir(local_path):
        abs_dir = local_path + '\\' + _dir
        if os.path.isdir(abs_dir):
            oss_map[abs_dir] = OssObject(abs_dir, NULL_MD5, time.mktime(time.gmtime()))
            _recursive_indexing(abs_dir, oss_map)
        else:
            oss_map[abs_dir] = OssObject(abs_dir, file_md5(abs_dir), os.path.getmtime(abs_dir))
    return oss_map


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


def local_to_remote(local, root_map_lr):
    """
    transfer local path to the corresponding remote path using directory map
    :param local:
    :param root_map_lr:
    :return:
    """
    assert root_map_lr[0] in local, 'local does not match local_root'
    rootl, rootr = root_map_lr[0], root_map_lr[1]
    common = local.split(rootl)[1]
    remote = rootr + common
    if len(os.path.splitext(remote)[-1]) == 0:
        remote += '/'
    remote = remote.replace('\\', '/')
    return remote


def remote_to_local(remote, root_map_lr):
    """
    transfer remote path to the corresponding local path using directory map
    :param remote:
    :param root_map_lr:
    :return:
    """
    assert root_map_lr[1] in remote, 'remote does not match remote_root'
    rootl, rootr = root_map_lr[0], root_map_lr[1]
    common = remote.split(rootr)[1]
    local = rootl + common
    local = local.replace('/', '\\')
    return local

