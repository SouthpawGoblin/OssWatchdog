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
import os

logger = logging.getLogger("main.objectManager")


class ObjectManager:
    """
    class for managing bucket objects
    """
    def __init__(self, bucket):
        self.bucket = bucket

    def object_exists(self, remote):
        """
        wrapper for Bucket.object_exists()
        :param remote:
        :return:
        """
        try:
            return self.bucket.object_exists(remote)
        except Exception as e:
            logger.error("object_exists error-- " + util.exception_string(e))
            return None

    def get_etag(self, remote):
        """
        get object etag
        :param remote:
        :return:
        """
        try:
            if self.object_exists(remote):
                return self.bucket.head_object(remote).etag
            return False
        except Exception as e:
            logger.error("get_etag error-- " + util.exception_string(e))
            return False

    def put_object(self, remote, local):
        """
        upload a file
        :param remote:
        :param local:
        :return:
        """
        # TODO: resumable support
        # TODO: progress report
        try:
            # 通过etag检测文件是否完全相同，避免不必要的流量消耗
            if self.object_exists(remote) and self.get_etag(remote) == util.file_md5(local):
                return False
            if os.path.isdir(local):
                return self.bucket.put_object(remote, '')
            else:
                return self.bucket.put_object_from_file(remote, local)
        except Exception as e:
            logger.error("put_object error-- " + util.exception_string(e))
            return False

    def get_object(self, remote, local):
        """
        download a file
        :param local:
        :param remote:
        :return:
        """
        # TODO: resumable support
        # TODO: progress report
        try:
            # 通过etag检测文件是否完全相同，避免不必要的流量消耗
            if os.path.exists(local) and self.get_etag(remote) == util.file_md5(local):
                return False
            result = self.bucket.get_object_to_file(remote, local)
            return result
        except Exception as e:
            logger.error("get_object error-- " + util.exception_string(e))
            return False

    def delete_object(self, remote):
        """
        delete a file
        :param remote:
        :return:
        """
        # TODO: progress report
        try:
            if self.object_exists(remote):
                self.bucket.delete_object(remote)
                return True
            else:
                return False
        except Exception as e:
            logger.error("delete_object error-- " + util.exception_string(e))
            return False

    def rename_object(self, remote_old, remote_new):
        """
        rename a file using Bucket.copy_object() first then delete the original
        :param remote_old:
        :param remote_new:
        :return:
        """
        # TODO: progress report
        try:
            if self.object_exists(remote_old):
                self.bucket.copy_object(self.bucket.bucket_name, remote_old, remote_new)
                self.delete_object(remote_old)
                return True
            else:
                return False
        except Exception as e:
            logger.error("rename_object error-- " + util.exception_string(e))
            return False

    def get_object_iter(self, prefix='', delimiter=''):
        """
        return object iterator with specified prefix and/or delimiter
        :param prefix:
        :param delimiter:
        :return:
        """
        try:
            return oss2.ObjectIterator(self.bucket, prefix, delimiter)
        except Exception as e:
            logger.error("get_object_iter error-- " + util.exception_string(e))
