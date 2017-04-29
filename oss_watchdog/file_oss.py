"""
class for manipulating objects
"""
from . import utils
from .file import BaseFileManager
import oss2
import os.path as path


class OssFileManager(BaseFileManager):
    """
    class for managing oss files
    """

    # since bucket.upload_file() may get 407 when content is empty,
    # I give all directory objects "$DIR$" as content
    LOCAL_DIR_CONTENT = "$DIR$"
    # MD5 of DIR_CONTENT, local folders will get this MD5 as etag, but md5 of a dir will never be used
    LOCAL_DIR_CONTENT_MD5 = utils.content_md5(LOCAL_DIR_CONTENT)

    MD5_HEADER_STRING = 'Content-MD5'

    def __init__(self, auth_key, auth_key_secret, endpoint, bucket_name):
        auth = oss2.Auth(auth_key, auth_key_secret)
        self.__bucket = oss2.Bucket(auth, endpoint, bucket_name, enable_crc=False)

    def get_md5(self, remote, *args, **kwargs):
        """
        try get file md5 from header 'Content-MD5',
        if failed return etag
        :param remote:
        :return:
        """
        try:
            remote = OssFileManager.remote_normpath(remote)
            head = self.__bucket.head_object(remote)
            if OssFileManager.MD5_HEADER_STRING in head.headers:
                return head.headers[OssFileManager.MD5_HEADER_STRING]
            else:
                return head.etag
        except Exception as e:
            raise e

    def file_exists(self, remote, *args, **kwargs):
        """
        wrapper for Bucket.object_exists()
        :param remote:
        :return:
        """
        try:
            remote = OssFileManager.remote_normpath(remote)
            return self.__bucket.object_exists(remote)
        except Exception as e:
            raise e

    def upload_file(self, local, remote, progress_callback=None, *args, **kwargs):
        """
        upload a file
        :param local:
        :param remote:
        :param progress_callback:
        :return: class:`PutObjectResult <oss2.models.PutObjectResult>`
        """
        # TODO: resumable support
        # TODO: multipart support
        try:
            remote = OssFileManager.remote_normpath(remote)
            local = path.abspath(local)
            if path.isdir(local):
                md5 = OssFileManager.LOCAL_DIR_CONTENT_MD5
                result = self.__bucket.put_object(remote, OssFileManager.LOCAL_DIR_CONTENT,
                                                  headers={OssFileManager.MD5_HEADER_STRING: md5},
                                                  progress_callback=progress_callback)
            else:
                md5 = utils.file_md5(local)
                result = self.__bucket.put_object_from_file(remote, local,
                                                            headers={OssFileManager.MD5_HEADER_STRING: md5},
                                                            progress_callback=progress_callback)
            print("object put | \"" + local + "\" --> \"" + remote + "\"")
            return result
        except Exception as e:
            raise e

    def download_file(self, remote, local, progress_callback=None, *args, **kwargs):
        """
        download a file
        :param remote:
        :param local:
        :param progress_callback:
        :return:
        """
        # TODO: resumable support
        # TODO: multipart support
        try:
            remote = OssFileManager.remote_normpath(remote)
            local = path.abspath(local)
            result = self.__bucket.get_object_to_file(remote, local,
                                                      progress_callback=progress_callback)
            print("object got | \"" + remote + "\" --> \"" + local + "\"")
            return result
        except Exception as e:
            raise e

    def delete_file(self, remote, *args, **kwargs):
        """
        delete a file
        :param remote:
        :return: class:`RequestResult <oss2.models.RequestResult>`
        """
        try:
            remote = OssFileManager.remote_normpath(remote)
            result = self.__bucket.delete_object(remote)
            print("object deleted | \"" + remote + "\"")
            return result
        except Exception as e:
            raise e

    def rename_file(self, remote_old, remote_new, *args, **kwargs):
        """
        rename a file using Bucket.copy_object() first then delete the original
        :param remote_old:
        :param remote_new:
        :return:
        """
        try:
            remote_old = OssFileManager.remote_normpath(remote_old)
            remote_new = OssFileManager.remote_normpath(remote_new)
            self.__bucket.copy_object(self.__bucket.bucket_name, remote_old, remote_new)
            self.delete_file(remote_old)
            print("object renamed | \"" + remote_old + "\" --> \"" + remote_new + "\"")
        except Exception as e:
            raise e

    def file_iterator(self, root='', delimiter='', *args, **kwargs):
        """
        return object iterator with specified prefix and/or delimiter
        :param root:
        :param delimiter:
        :return:
        """
        try:
            return oss2.ObjectIterator(self.__bucket, root, delimiter)
        except Exception as e:
            raise e

    @staticmethod
    def remote_normpath(remote_path):
        """
        normalize remote path
        e.g. foo/bar/ --directory
        e.g. foo/bar/foobar.txt --file
        :param remote_path:
        :return:
        """
        isdir = True if remote_path.endswith(('\\', '/')) else False
        remote_path = path.normpath(remote_path).replace('\\', '/')
        if isdir:
            remote_path += '/'
        return remote_path

    @staticmethod
    def remote_isdir(remote_path):
        """
        judge if a remote_path is a dir by if it ends with '/'
        :param remote_path:
        :return:
        """
        return OssFileManager.remote_normpath(remote_path).endswith('/')