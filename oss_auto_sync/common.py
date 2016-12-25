# -*- coding: utf-8 -*-

"""
common classes
"""
import os.path as path
from . import utils
import time


class SyncParams(object):
    """
    data structure for a local-remote pair
    """
    def __init__(self, auth_key, auth_key_secret, endpoint,
                 bucket_name, local_path, remote_path):
        """
        :param auth_key:
        :param auth_key_secret:
        :param endpoint:
        :param bucket_name:
        :param local_path: local root path
        :param remote_path: remote root path
        """
        self.__auth_key = auth_key
        self.__auth_key_secret = auth_key_secret
        self.__endpoint = endpoint
        self.__bucket_name = bucket_name
        self.__local_path = local_path
        self.__remote_path = remote_path

    @property
    def auth_key(self):
        return self.__auth_key

    @property
    def auth_key_secret(self):
        return self.__auth_key_secret

    @property
    def endpoint(self):
        return self.__endpoint

    @property
    def bucket_name(self):
        return self.__bucket_name

    @property
    def local_path(self):
        return self.__local_path

    @property
    def remote_path(self):
        return self.__remote_path


class LocalObject(object):
    """
    class representing a local file or directory
    """
    def __init__(self, local_path):
        self.__path = path.abspath(local_path)
        self.__is_dir = path.isdir(local_path)
        self.__md5 = utils.file_md5(local_path).upper()
        self.__lmt = path.getmtime(local_path)
        self.__size = path.getsize(self.__path)

    @property
    def path(self):
        return self.__path

    @property
    def md5(self):
        return self.__md5

    @property
    def last_modified(self):
        return self.__lmt

    @property
    def is_dir(self):
        return self.__is_dir

    @property
    def size(self):
        return self.__size
# class Printer:
#     """
#     general info or error printer
#     """
#     def __init__(self, err_logger=None):
#         self.__err_logger = err_logger
#
#     def print(self, msg):
#         """
#         print msg to predefined logger or sys.stdout
#         :param msg: if msg is Exception, print to logger; else print to stdout
#         :return:
#         """
#         if msg is Exception and self.__err_logger is not None:
#             self.__err_logger.error(str(msg))
#         else:
#             print(str(msg))
