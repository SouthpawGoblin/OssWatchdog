# -*- coding: utf-8 -*-

import src.object_manager as om
import config.config3 as config
from watchdog.events import *
import src.oss2_utils as util

ROOT_LOCAL = config.directory_mapping.keys()
ROOT_REMOTE = config.directory_mapping.values()
mapping = config.directory_mapping

logger = logging.getLogger("main.watchdogImpl")


class FileEventHandler(FileSystemEventHandler):
    def __init__(self, bucket):
        FileSystemEventHandler.__init__(self)
        self.ob_manager = om.ObjectManager(bucket)

    def on_moved(self, event):
        """重命名"""
        try:
            remote_old = util.local_to_remote(event.src_path, mapping)
            remote_new = util.local_to_remote(event.dest_path, mapping)
            if not self.ob_manager.rename_object(remote_old, remote_new):
                # 若原文件不存在则直接put新文件
                self.ob_manager.put_object(remote_new, event.dest_path)
            print("file moved from {0} to {1}".format(event.src_path, event.dest_path))
        except Exception as e:
            logger.error("rename error-- " + util.exception_string(e))

    def on_created(self, event):
        """新建"""
        remote = util.local_to_remote(event.src_path, mapping)
        self.ob_manager.put_object(remote, event.src_path)
        print("file created:{0}".format(event.src_path))

    def on_deleted(self, event):
        """删除"""
        remote = util.local_to_remote(event.src_path, mapping)
        self.ob_manager.delete_object(remote)
        print("file deleted:{0}".format(event.src_path))
