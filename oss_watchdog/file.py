"""
base class for manipulating objects
"""


class BaseFileManager:
    def get_md5(self, src, *args, **kwargs):
        pass

    def file_exists(self, src, *args, **kwargs):
        pass

    def upload_file(self, src, dest, on_success=None, on_error=None, *args, **kwargs):
        pass

    def download_file(self, src, dest, on_success=None, on_error=None, *args, **kwargs):
        pass

    def delete_file(self, src, on_success=None, on_error=None, *args, **kwargs):
        pass

    def rename_file(self, src_old, src_new, on_success=None, on_error=None, *args, **kwargs):
        pass

    def file_iterator(self, root, *args, **kwargs):
        pass

