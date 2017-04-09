# -*- coding: utf-8 -*-
"""
YuiSync exceptions
"""


class YuiException(Exception):
    """
    base exception for all custom exceptions
    """
    pass


class TaskStoptimeException(YuiException):
    """
    raised when a task encounters errors while stopping
    """
    pass