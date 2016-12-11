# -*- coding: utf-8 -*-

"""
common classes
"""


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


class Printer:
    """
    general info or error printer
    """
    def __init__(self, err_logger=None):
        self.__err_logger = err_logger

    def print(self, msg):
        """
        print msg to predefined logger or sys.stdout
        :param msg: if msg is Exception, print to logger; else print to stdout
        :return:
        """
        if msg is Exception and self.__err_logger is not None:
            self.__err_logger.error(str(msg))
        else:
            print(str(msg))
