# -*- coding: utf-8 -*-

"""
utils
"""
import hashlib
import base64
import requests
import time
import os.path as path


def get_server_time():
    """
    get server time (GMT timestamp)
    :return:
    """
    response = requests.get('http://www.aliyun.com')
    t = response.headers.get('date')
    time_tuple = time.strptime(t[5:25], "%d %b %Y %H:%M:%S")
    stamp = int(time.mktime(time_tuple))
    return stamp


def file_md5(file_name, block_size=64 * 1024):
    """计算文件的MD5
    :param file_name: 文件名
    :param block_size: 计算MD5的数据块大小，默认64KB
    :return 文件内容的MD5值
    """
    with open(file_name, 'rb') as f:
        md5 = hashlib.md5()
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)

    return base64.b64encode(md5.digest()).decode()


def content_md5(data):
    """计算数据的MD5
    :param data: 数据
    :return MD5值
    """
    md5 = hashlib.md5()
    md5.update(str(data).encode())
    return base64.b64encode(md5.digest()).decode()


def dir_md5(dir_path):
    """
    calculate directory md5 (upper case)
    :param dir_path:
    :return:
    """
    pass


if __name__ == "__main__":
    print(content_md5("$DIR$"))
