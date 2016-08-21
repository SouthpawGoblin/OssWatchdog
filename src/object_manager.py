# -*- coding: utf-8 -*-

import src.oss2_utils as util
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

    def put_file(self, remote, local):
        """
        upload a file
        :param remote:
        :param local:
        :return:
        """
        try:
            if self.object_exists(remote) and self.get_etag(remote) == util.file_md5(local):
                return False
            result = self.bucket.put_object_from_file(remote, local)
            return result
        except Exception as e:
            logger.error("put_file error-- " + util.exception_string(e))
            return False

    def get_file(self, remote, local):
        """
        download a file
        :param local:
        :param remote:
        :return:
        """
        try:
            if os.path.exists(local) and self.get_etag(remote) == util.file_md5(local):
                return False
            result = self.bucket.get_object_to_file(remote, local)
            return result
        except Exception as e:
            logger.error("get_file error-- " + util.exception_string(e))
            return False

    def delete_file(self, remote):
        """
        delete a file
        :param remote:
        :return:
        """
        try:
            if self.object_exists(remote):
                self.bucket.delete_object(remote)
                return True
            else:
                return False
        except Exception as e:
            logger.error("delete_file error-- " + util.exception_string(e))
            return False

    def rename_file(self, remote_old, remote_new):
        """
        rename a file using Bucket.copy_object() first then delete the original
        :param remote_old:
        :param remote_new:
        :return:
        """
        try:
            if self.object_exists(remote_old):
                self.bucket.copy_object(self.bucket.bucket_name, remote_old, remote_new)
                self.delete_file(remote_old)
                return True
            else:
                return False
        except Exception as e:
            logger.error("rename_file error-- " + util.exception_string(e))
            return False
