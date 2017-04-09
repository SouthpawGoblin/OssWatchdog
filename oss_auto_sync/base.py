# -*- coding: utf-8 -*-

"""
base abstract classes
"""


class CommonPath:
    """
    data structure representing a file path
    stores information about whether the file is local or remote   
    """
    def __init__(self, is_local, path_str):
        self._is_local = is_local
        self._path = path_str

    def __str__(self):
        return str(self._path)

    @property
    def is_local(self):
        return self._is_local


class CommonFile:
    """
    data structure representing a file
    Note: use `is_local` to distinguish local file from remote
    """
    def __init__(self, path):
        """
        :param path: should be an instance of a <CommonPath>'s subclass
        """
        if not issubclass(type(path), CommonPath):
            raise TypeError("path should be an instance of a <CommonPath>'s subclass")
        self._path = path

    @property
    def path(self):
        return self._path

    @property
    def is_local(self):
        return self._path.is_local

    def get_size(self):
        """
        get remote file size
        override this
        :return: 
        """
        pass

    def get_etag(self):
        """
        get remote file's unique id, eg. md5
        should be stringifiable
        override this
        :return: 
        """
        pass

    def is_dir(self):
        """
        should return boolean value
        override this
        :return: 
        """
        pass

    def get_last_modified_time(self):
        """
        should be of type <datetime.datetime>
        override this
        :return: 
        """
        pass


class FileManager:
    """
    maintains multiple file operation methods
    <Monitor> will use this to manipulate file and directories
    """