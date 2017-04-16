# -*- coding: utf-8 -*-

"""
base classes
"""


class MetaFile(object):
    """
    data structure stores file meta info
    """
    def __init__(self, path, size, hashcode, is_dir, last_modified_time):
        self._path = path
        self._size = size
        self._hash = hashcode
        self._is_dir = is_dir
        self._lmt = last_modified_time

    @property
    def path(self):
        return str(self._path)

    @property
    def size(self):
        return self._size

    @property
    def hashcode(self):
        return self._hash

    @property
    def is_dir(self):
        return self._is_dir

    @property
    def last_modified_time(self):
        return self._lmt


class BaseFileManager(object):
    """
    maintains necessary file operation methods
    <Monitor> will use this to manipulate file and directories
    """
    def __init__(self, manager_type="UNDEFINED"):
        """
        :param manager_type: a string representing manager type, default is "UNDEFINED" 
        """
        self._manager_type = manager_type

    @property
    def manager_type(self):
        return self._manager_type

    def get_meta_info(self, path):
        """
        get object meta info
        :param path:
        :return: should be an instance of <MetaFile>
        """
        return MetaFile(path, None, None, None, None)

    def is_exist(self, path):
        """
        :param path:
        :return:
        """
        pass

    def upload(self, src_path, dest_path):
        """
        upload a file
        :param src_path: 
        :param dest_path: 
        :return: 
        """
        pass

    def download(self, src_path, dest_path):
        """
        download a file
        :param src_path:
        :param dest_path:
        :return:
        """
        pass

    def delete(self, path):
        """
        delete a file
        :param path:
        :return:
        """
        pass

    def move(self, src_path, dest_path):
        """
        move a file
        :param src_path:
        :param dest_path:
        :return:
        """
        pass

    def iter_files(self, root_path):
        """
        return file iterator
        :param root_path:
        :return:
        """
        pass

    def path_remote_to_local(self, path):
        """
        transfer remote path to local path format
        :param path: 
        :return: 
        """
        pass

    def path_local_to_remote(self, path):
        """
        transfer local path to remote path format
        :param path: 
        :return: 
        """