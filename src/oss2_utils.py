# -*- coding: utf-8 -*-

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
