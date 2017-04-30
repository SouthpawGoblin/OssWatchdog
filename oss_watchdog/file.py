"""
base class for manipulating objects
"""


class BaseFileManager:
    def get_md5(self, src, *args, **kwargs):
        pass

    def is_exist(self, src, *args, **kwargs):
        pass

    def upload(self, src, dest, recursive=False, on_success=None, on_error=None, *args, **kwargs):
        pass

    def download(self, src, dest, recursive=False, on_success=None, on_error=None, *args, **kwargs):
        pass

    def delete(self, src, recursive=False, on_success=None, on_error=None, *args, **kwargs):
        pass

    def rename(self, src_old, src_new, on_success=None, on_error=None, *args, **kwargs):
        pass

    def get_iterator(self, root, *args, **kwargs):
        pass

    @staticmethod
    def norm_path(src):
        pass

    @staticmethod
    def is_dir(src):
        pass

