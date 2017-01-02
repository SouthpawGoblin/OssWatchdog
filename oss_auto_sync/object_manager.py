"""
class for manipulating objects
"""
from . import utils
from .common import LocalObject
import oss2
import os.path as path


class ObjectManager:
    """
    class for managing bucket objects
    """

    MD5_HEADER_STRING = 'Content-MD5'
    LMT_HEADER_STRING = 'x-oss-meta-lmt'

    def __init__(self, bucket):
        self.__bucket = bucket

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

    def get_md5(self, remote):
        """
        try get file md5 from header 'Content-MD5',
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

    # def _update_md5(self, remote, md5):
    #     """
    #     update remote object's md5
    #     :param remote:
    #     :param md5:
    #     :return:
    #     """
    #     try:
    #         remote = utils.remote_normpath(remote)
    #         self.__bucket.update_object_meta(remote, {ObjectManager.MD5_HEADER_STRING: md5})
    #     except Exception as e:
    #         raise e

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

    def put_object(self, remote, local, progress_callback=None):
        """
        upload a file
        :param remote:
        :param local:
        :param progress_callback:
        :return:
        """
        # TODO: resumable support
        try:
            remote = utils.remote_normpath(remote)
            local = path.abspath(local)
            if path.isdir(local):
                md5 = LocalObject.DIR_CONTENT_MD5
                self.__bucket.put_object(remote, LocalObject.DIR_CONTENT,
                                         headers={ObjectManager.MD5_HEADER_STRING: md5},
                                         progress_callback=progress_callback)
            else:
                md5 = utils.file_md5(local)
                if not self.object_exists(remote) or self.get_md5(remote) != md5:
                    self.__bucket.put_object_from_file(remote, local,
                                                       headers={ObjectManager.MD5_HEADER_STRING: md5},
                                                       progress_callback=progress_callback)
            print("object put | \"" + local + "\" --> \"" + remote + "\"")
        except Exception as e:
            raise e

    def get_object(self, remote, local, progress_callback=None):
        """
        download a file
        :param remote:
        :param local:
        :param progress_callback:
        :return:
        """
        # TODO: resumable support
        try:
            remote = utils.remote_normpath(remote)
            local = path.abspath(local)
            if path.exists(local):
                if path.isdir(local) or self.get_md5(remote) == utils.file_md5(local):
                    return
            self.__bucket.get_object_to_file(remote, local,
                                             progress_callback=progress_callback)
            print("object got | \"" + remote + "\" --> \"" + local + "\"")
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
