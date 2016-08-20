# -*- coding: utf-8 -*-

import config.config as config
import src.oss2_utils as util
import logging
import oss2

logger = logging.getLogger("main.objectManager")


def put_file(bucket, dest, src):
    """
    upload a file
    :param bucket:
    :param dest:
    :param src:
    :return:
    """
    try:
        result = bucket.put_object_from_file(dest, src)
        return result
    except Exception as e:
        logger.error("put_file error-- " + util.exception_string(e))
        return None


def get_file(bucket, dest, src):
    """
    download a file
    :param bucket:
    :param dest:
    :param src:
    :return:
    """
    try:
        result = bucket.get_object_to_file(src, dest)
        return result
    except Exception as e:
        logger.error("get_file error-- " + util.exception_string(e))
        return None


def delete_file(bucket, src):
    """
    delete a file
    :param bucket:
    :param src:
    :return:
    """
    try:
        bucket.delete_object(src)
    except Exception as e:
        logger.error("delete_file error-- " + util.exception_string(e))