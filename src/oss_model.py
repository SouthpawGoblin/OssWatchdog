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
import oss2
import logging
import time
import os

logger = logging.getLogger("main.ossModel")

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
#         self.__loc_path = relative_path
#         self.__etag = etag
#         self.__lmt = last_modified_time
#         self.__father = None
#         self.__children = set([])
#
#     def __eq__(self, other):
#         if not other.__loc_path or other.__loc_path != self.__loc_path:
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
#         return self.__loc_path
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
#         return len(os.path.splitext(self.__loc_path)[-1]) == 0
#
#     def add_child(self, node):
#         """
#         :param node:
#         :return:
#         """
#         if node.__loc_path and node.__etag and node.__lmt:
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

    def __init__(self, local_path):
        """
        :param local_path:
        """
        if not os.path.exists(local_path):
            raise FileNotFoundError
        self.__loc_path = local_path
        self.__is_dir = os.path.isdir(local_path)
        self.__etag = NULL_MD5 if self.__is_dir else util.file_md5(local_path)
        self.__lmt = time.gmtime() if self.__is_dir else os.path.getmtime(local_path)

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
