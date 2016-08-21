# -*- coding: utf-8 -*-

from hashlib import md5
import oss2


def exception_string(e):
    """
    transfer OssError into string
    :param e:
    :return:
    """
    if e is oss2.exceptions.OssError:
        return "OssError: status= " + e.status + \
               "||request_id= " + e.request_id + \
               "||code= " + e.code + \
               "||message= " + e.message
    else:
        return str(e)


def file_md5(file):
    """
    calculation file md5 (upper case)
    :param file:
    :return:
    """
    m = md5()
    a_file = open(file, 'rb')  # 需要使用二进制格式读取文件内容
    m.update(a_file.read())
    a_file.close()
    return m.hexdigest().upper()


def local_to_remote(local, mapping):
    """
    transfer local path to the corresponding remote path using directory map
    :param local:
    :param mapping:
    :return:
    """
    rootl, rootr = None
    for k, v in mapping.items():
        if k in local:
            rootl, rootr = k, v
            break
    if rootl is None or rootr is None:
        raise Exception("No local root matches!")
    common = local.split(rootl)[1]
    remote = rootr + "/" + common[1:]
    return remote


def remote_to_local(remote, mapping):
    """
    transfer remote path to the corresponding local path using directory map
    :param remote:
    :param mapping:
    :return:
    """
    rootl, rootr = None
    for k, v in mapping.items():
        if v in remote:
            rootl, rootr = k, v
            break
    if rootl is None or rootr is None:
        raise Exception("No remote root matches!")
    common = remote.split(rootr)[1]
    local = rootl + "\\" + common[1:]
    return local
