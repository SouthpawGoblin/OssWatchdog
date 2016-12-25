"""
class for manipulating objects
"""
from . import utils
import oss2
import os.path as path


class ObjectManager:
    """
    class for managing bucket objects
    """

    MD5_HEADER_STRING = 'x-oss-meta-md5'

    def __init__(self, bucket, progress_callback=None):
        self.__bucket = bucket
        self.__progress_callback = progress_callback

    def _get_etag(self, remote):
        """
        get object etag
        :param remote:
        :return:
        """
        try:
            remote = utils.remote_normpath(remote)
            return self.__bucket.head_object(remote).etag
        except Exception as e:
            raise e

    def _get_md5(self, remote):
        """
        try get file md5 from header 'x-oss-meta-md5',
        if failed return etag
        :param remote:
        :return:
        """
        try:
            remote = utils.remote_normpath(remote)
            headers = self.__bucket.head_object(remote).headers
            if ObjectManager.MD5_HEADER_STRING in headers:
                return headers[ObjectManager.MD5_HEADER_STRING]
            else:
                return self._get_etag(remote)
        except Exception as e:
            raise e

    def _update_md5(self, remote, md5):
        """
        update remote object's md5
        :param remote:
        :param md5:
        :return:
        """
        try:
            remote = utils.remote_normpath(remote)
            self.__bucket.update_object_meta(remote, {ObjectManager.MD5_HEADER_STRING: md5})
        except Exception as e:
            raise e

    def object_exists(self, remote):
        """
        wrapper for Bucket.object_exists()
        :param remote:
        :return:
        """
        try:
            remote = utils.remote_normpath(remote)
            return self.__bucket.object_exists(remote)
        except Exception as e:
            raise e

    def put_object(self, remote, local, md5=None, enable_callback=True):
        """
        upload a file
        supports custom md5,
        if md5 == None, calculate using utils.file_md5() or utils.dir_md5()
        :param remote:
        :param local:
        :param md5:
        :param enable_callback:
        :return:
        """
        # TODO: resumable support
----->  添加md5回溯更新
        try:
            remote = utils.remote_normpath(remote)
            local = path.abspath(local)
            if path.isdir(local):
                md5 = md5 if md5 else utils.dir_md5(local)
                self.__bucket.put_object(remote, '',
                                         headers={ObjectManager.MD5_HEADER_STRING: md5},
                                         progress_callback=self.__progress_callback if enable_callback else None)
            elif not self.object_exists(remote) or self._get_md5(remote) != utils.file_md5(local):
                md5 = md5 if md5 else utils.file_md5(local)
                self.__bucket.put_object_from_file(remote, local,
                                                   headers={ObjectManager.MD5_HEADER_STRING: md5},
                                                   progress_callback=self.__progress_callback if enable_callback else None)
            print("object put | \"" + local + "\" --> \"" + remote + "\"")
        except Exception as e:
            raise e

    def get_object(self, remote, local, enable_callback=True):
        """
        download a file
        :param remote:
        :param local:
        :param enable_callback:
        :return:
        """
        # TODO: resumable support
        try:
            remote = utils.remote_normpath(remote)
            local = path.abspath(local)
            if path.exists(local):
                if path.isdir(local) or self._get_md5(remote) == utils.file_md5(local):
                    return
            self.__bucket.get_object_to_file(remote, local,
                                             progress_callback=self.__progress_callback if enable_callback else None)
            print("object got | \"" + remote + "\" --> \"" + local + "\"")
            return
        except Exception as e:
            raise e

    def delete_object(self, remote):
        """
        delete a file
        :param remote:
        :return:
        """
        try:
            remote = utils.remote_normpath(remote)
            if self.object_exists(remote):
                self.__bucket.delete_object(remote)
                print("object deleted | \"" + remote + "\"")
            return
        except Exception as e:
            raise e

    def rename_object(self, remote_old, remote_new):
        """
        rename a file using Bucket.copy_object() first then delete the original
        :param remote_old:
        :param remote_new:
        :return:
        """
        try:
            remote_old = utils.remote_normpath(remote_old)
            remote_new = utils.remote_normpath(remote_new)
            self.__bucket.copy_object(self.__bucket.bucket_name, remote_old, remote_new)
            self.delete_object(remote_old)
            print("object renamed | \"" + remote_old + "\" --> \"" + remote_new + "\"")
            return
        except Exception as e:
            raise e

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
            raise e
