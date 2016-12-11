# -*- coding: utf-8 -*-

"""
file system monitors
"""

from watchdog.observers import Observer
from watchdog.events import *
from .common import SyncParams
from.common import Printer


class SyncSocket(FileSystemEventHandler):
    """
    class representing a local-remote sync link
    """
    def __init__(self, sync_param):
        FileSystemEventHandler.__init__(self)
        self.__bucket = bucket
        self.__local_remote_tup = local_remote_tup
        self.__obj_manager = ObjectManager(bucket, self._task_percentage)
        self.__local_index = self._local_indexing()
        self.__is_synchronizing = False
        self.__sync_queue = []
        self.__total_task_cnt = 0
        self.__fin_task_cnt = 0

    def on_moved(self, event):
        """rename"""
        try:
            if self.__is_synchronizing:
                self.__sync_queue.append(('on_moved', event))
                return
            remote_old = self.__local_to_remote(event.src_path)
            remote_new = self.__local_to_remote(event.dest_path)
            if not self.__obj_manager.rename_object(remote_old, remote_new):
                # put new file if old file does not exist
                self.__obj_manager.put_object(remote_new, event.dest_path)
        except Exception as e:
            logger_err.error("rename error-- " + util.exception_string(e))

    # def on_created(self, event):
    #     """create"""
    #     remote = self.__local_to_remote(event.src_path)
    #     self.__obj_manager.put_object(remote, event.src_path)
    #     logger_main.info("file created:{0}".format(event.src_path))

    def on_deleted(self, event):
        """delete"""
        if self.__is_synchronizing:
            self.__sync_queue.append(('on_deleted', event))
            return
        remote = self.__local_to_remote(event.src_path)
        self.__obj_manager.delete_object(remote)

    def on_modified(self, event):
        """
        modify
        :param event:
        :return:
        """
        if self.__is_synchronizing:
            self.__sync_queue.append(('on_modified', event))
            return
        remote = self.__local_to_remote(event.src_path)
        self.__obj_manager.put_object(remote, event.src_path)

    def is_name_equal(self, local_obj, remote_obj):
        """
        :param local_obj: local file object, should be of type OssObject
        :param remote_obj: remote oss object, should be of type SimplifiedObjectInfo
        :return:
        """
        if not type(local_obj) is OssObject:
            raise TypeError('local_obj should be of type OssObject')
        if not type(remote_obj) is SimplifiedObjectInfo:
            raise TypeError('remote_obj should be of type SimplifiedObjectInfo')
        return self.__local_to_remote(local_obj.key) == remote_obj.key

    def is_content_equal(self, local_obj, remote_obj):
        """
        :param local_obj: local file object, should be of type OssObject
        :param remote_obj: remote oss object, should be of type SimplifiedObjectInfo
        :return:
        """
        if not type(local_obj) is OssObject:
            raise TypeError('local_obj should be of type OssObject')
        if not type(remote_obj) is SimplifiedObjectInfo:
            raise TypeError('remote_obj should be of type SimplifiedObjectInfo')
        return local_obj.etag == remote_obj.etag

    def synchronize(self):
        """
        synchronize local_path with the remote bucket
        :return:
        """
        self.__is_synchronizing = True
        # get remote objects
        remote_iter = self.__obj_manager.get_object_iter(self.__local_remote_tup[1] + '/')

        tmp_set = set([])
        for obj in remote_iter:
            local_key = self.__remote_to_local(obj.key)
            if local_key in self.__local_index:   # both have this file
                local_obj = self.__local_index[local_key]
                if not self.is_content_equal(local_obj, obj):   # different content
                    if local_obj.last_modified >= obj.last_modified:    # local is newer
                        self.__obj_manager.put_object(obj.key, local_key)
                    else:                                               # remote is newer
                        self.__obj_manager.get_object(obj.key, local_key)
            else:
                if os.path.isdir(local_key):
                    if not os.path.exists(local_key):
                        os.makedirs(local_key)
                else:
                    tmp_dir = local_key[:local_key.rfind('\\')]
                    if not os.path.exists(tmp_dir):
                        os.makedirs(tmp_dir)
                    self.__obj_manager.get_object(obj.key, local_key)
            tmp_set.add(local_key)

        for local_key in self.__local_index:
            if local_key not in tmp_set:
                self.__obj_manager.put_object(self.__local_to_remote(local_key), local_key)
        self.__is_synchronizing = False

        while len(self.__sync_queue) > 0:
            pair = self.__sync_queue.pop(0)
            if pair[0] == 'on_moved':
                self.on_moved(pair[1])
            elif pair[0] == 'on_deleted':
                self.on_deleted(pair[1])
            elif pair[0] == 'on_modified':
                self.on_modified(pair[1])

    def _local_indexing(self):
        """
        generate local file index map {local_path: OssObject}
        :return:
        """
        oss_map = self._recursive_indexing(self.__local_remote_tup[0], None)
        return oss_map

    def _recursive_indexing(self, local_path, oss_map):
        if not oss_map:
            oss_map = {}
        for _dir in os.listdir(local_path):
            abs_dir = os.path.join(local_path, _dir)
            if not os.path.isdir(abs_dir):
                oss_map[abs_dir] = OssObject(abs_dir)
            else:
                oss_map[os.path.join(abs_dir, '')] = OssObject(abs_dir)
                self._recursive_indexing(abs_dir, oss_map)
            print(abs_dir)
        return oss_map

    def __local_to_remote(self, local_path, is_dir=None):
        """
        transfer local path to the corresponding remote path using directory map
        :param local_path:
        :param is_dir   if None, use os.path.isdir()
        :return:
        """
        local_path = local_path.strip().strip('\\')
        rootl, rootr = self.__local_remote_tup[0], self.__local_remote_tup[1]
        rootl_re = rootl.replace('\\', '\\\\')
        pt = re.compile(r"^" + rootl_re)
        if not pt.match(local_path):
            raise FileNotFoundError('local_path does not belong to this root')

        common = local_path[len(rootl):]
        remote = rootr + common
        if is_dir or os.path.isdir(local_path):
            remote += '/'
        remote = remote.replace('\\', '/')
        return remote

    def __remote_to_local(self, remote_path):
        """
        transfer remote path to the corresponding local path using directory map
        :param remote_path:
        :return:
        """
        remote_path = remote_path.strip()
        rootl, rootr = self.__local_remote_tup[0], self.__local_remote_tup[1]
        pt = re.compile(r"^" + rootr)
        if not pt.match(remote_path):
            raise FileNotFoundError('remote_path does not belong to this root')

        common = remote_path[len(rootr):]
        local = rootl + common
        local = local.replace('/', '\\')
        return local

    def _task_percentage(self, consumed_bytes, total_bytes):
        """
        progress callback for uploading and downloading files
        :param consumed_bytes:
        :param total_bytes:
        :return:
        """
        if total_bytes:
            rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
            sys.stdout.write('\r{0}% '.format(rate))
            sys.stdout.flush()

    def _update_task_cnt(self, fin=False, total=False):
        """
        update fin and/or total count of tasks
        :param fin:
        :param total:
        :return:
        """
        if self.__fin_task_cnt == self.__total_task_cnt:
            self.__fin_task_cnt = 0
            self.__total_task_cnt = 0
        if total:
            self.__total_task_cnt += 1
        if fin:
            self.__fin_task_cnt += 1
        if self.__fin_task_cnt > self.__total_task_cnt:
            self.__fin_task_cnt = self.__total_task_cnt

    def _show_task_progress(self, discription=''):
        """
        show task progress
        :return:
        """
        sys.stdout.write('\r' + discription + ' {0}/{1} '.format(self.__fin_task_cnt, self.__total_task_cnt))
        sys.stdout.flush()


class Monitor(object):
    """
    a local-remote sync monitor
    """

    def __init__(self, sync_param, error_logger=None):
        """
        :param sync_param: should be of type SyncParams
        """
        if sync_param is not SyncParams:
            raise TypeError('sync_param should be of type oss_auto_sync.SyncParams')
        self.__sync_param = sync_param
        self.__socket = None
        self.__observer = None
        self.__printer = Printer(error_logger)

    def initialize(self):
        """
        create sync_socket and init watchdog observer
        :return:
        """
        try:
            self.__socket = SyncSocket(self.__sync_param)
            observer = Observer()
            observer.schedule(self.__socket, self.__sync_param.local_path, True)
            self.__observer = observer
        except Exception as e:
            self.__printer.print(e)
            raise e

    def run(self):
        """
        start the observer, synchronize local with remote
        :return:
        """
        try:
            if self.__observer is None:
                raise ValueError("Monitor must initialize before running")
            self.__observer.start()
            self.__socket.synchronize()
        except Exception as e:
            self.__printer.print(e)
            raise e

    def stop(self):
        """
        stop the observer
        :return:
        """
        try:
            # TODO: stop synchronize() as well if is in process
            self.__observer.stop()
            self.__observer.join()
        except Exception as e:
            self.__printer.print(e)
            raise e


class MonitorHub(object):
    """
    collection of Monitors, aim to control them at the same time
    """
    def __init__(self, sync_params, error_logger=None):
        """
        :param sync_params: should be an iterable of type SyncParam
        """
        self.__sync_params = sync_params
        self.__monitors = []
        self.__printer = Printer(error_logger)

    def initialize(self):
        """
        :return:
        """
        try:
            self.__monitors = [Monitor(param) for param in self.__sync_params]
        except Exception as e:
            self.__printer.print(e)
            raise e

    def run(self):
        """
        start all monitors
        :return:
        """
        try:
            [monitor.run() for monitor in self.__monitors]
        except Exception as e:
            self.__printer.print(e)
            raise e

    def stop(self):
        """
        stop all monitors
        :return:
        """
        try:
            [monitor.stop() for monitor in self.__monitors]
        except Exception as e:
            self.__printer.print(e)
            raise e
# TODO: 写个装饰器来wrap try-catch操作