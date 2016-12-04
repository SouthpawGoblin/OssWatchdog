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
from src.oss_model import OssObject
import oss2
import logging
import os

logger_main = logging.getLogger("main_logger")
logger_err = logging.getLogger('err_logger')


class ObjectManager:
    """
    class for managing bucket objects
    """
    def __init__(self, bucket, progress_callback=None):
        self.__bucket = bucket
        self.__progress_callback = progress_callback

    def object_exists(self, remote):
        """
        wrapper for Bucket.object_exists()
        :param remote:
        :return:
        """
        try:
            return self.__bucket.object_exists(remote)
        except Exception as e:
            logger_err.error("object_exists error | " + remote + " | " + util.exception_string(e))
            return None

    def get_etag(self, remote):
        """
        get object etag
        :param remote:
        :return:
        """
        try:
            if self.object_exists(remote):
                return self.__bucket.head_object(remote).etag
            return False
        except Exception as e:
            logger_err.error("get_etag error | " + remote + " | " + util.exception_string(e))
            return False

    def put_object(self, remote, local):
        """
        upload a file
        :param remote:
        :param local:
        :return:
        """
        # TODO: resumable support
        try:
            # 通过etag检测文件是否完全相同，避免不必要的流量消耗
            if self.object_exists(remote) and self.get_etag(remote) == OssObject(local).etag:
                return True
            if os.path.isdir(local):
                self.__bucket.put_object(remote, OssObject.DIR_CONTENT, progress_callback=self.__progress_callback)
            else:
                self.__bucket.put_object_from_file(remote, local, progress_callback=self.__progress_callback)
            logger_main.info("object put | \"" + local + "\" --> \"" + remote + "\"")
            return True
        except Exception as e:
            logger_err.error("put_object error | " + local + " | " + util.exception_string(e))
            return False

    def get_object(self, remote, local):
        """
        download a file
        :param local:
        :param remote:
        :return:
        """
        # TODO: resumable support
        try:
            # 通过etag检测文件是否完全相同，避免不必要的流量消耗
            if os.path.exists(local) and self.get_etag(remote) == util.file_md5(local):
                return True
            self.__bucket.get_object_to_file(remote, local, progress_callback=self.__progress_callback)
            logger_main.info("object got | \"" + remote + "\" --> \"" + local + "\"")
            return True
        except Exception as e:
            logger_err.error("get_object error | " + remote + " | " + util.exception_string(e))
            return False

    def delete_object(self, remote):
        """
        delete a file
        :param remote:
        :return:
        """
        try:
            if self.object_exists(remote):
                self.__bucket.delete_object(remote)
                logger_main.info("object deleted | \"" + remote + "\"")
            return True
        except Exception as e:
            logger_err.error("delete_object error | " + remote + " | " + util.exception_string(e))
            return False

    def rename_object(self, remote_old, remote_new):
        """
        rename a file using Bucket.copy_object() first then delete the original
        :param remote_old:
        :param remote_new:
        :return:
        """
        try:
            self.__bucket.copy_object(self.__bucket.bucket_name, remote_old, remote_new)
            self.delete_object(remote_old)
            logger_main.info("object renamed | \"" + remote_old + "\" --> \"" + remote_new + "\"")
            return True
        except Exception as e:
            logger_err.error("rename_object error | " + remote_old + " | " + util.exception_string(e))
            return False

    def get_object_iter(self, prefix='', delimiter=''):
        """
        return object iterator with specified prefix and/or delimiter
        :param prefix:
        :param delimiter:
        :return:
        """
        try:
            return oss2.ObjectIterator(self.__bucket, prefix, delimiter)
        except Exception as e:
            logger_err.error("get_object_iter error | " + prefix + " | " + delimiter + " | " + util.exception_string(e))
