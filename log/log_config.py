# -*- coding: utf-8 -*-

# Copyright 2016 Qi Yinzhe(Yinzhe-Qi) <goblin-qyz@163.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import datetime

config = {
    'version': 1,
    'formatters': {
        'info_formatter': {
            'class': 'logging.Formatter',
            'format': '| %(asctime)s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'err_formatter': {
            'class': 'logging.Formatter',
            'format': '| %(asctime)s | %(filename)s | line: %(lineno)d | %(levelname)s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'info_formatter',
            'level': 'INFO',
            'stream': 'ext://sys.stdout'
        },
        'file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'err_formatter',
            'level': 'ERROR',
            'filename': r'log\log_' + datetime.datetime.now().strftime('%Y%m%d') + r'.log',
            'maxBytes': 3 * 1024 * 1024,
            'backupCount': 3
        }
    },
    'loggers': {
        'main_logger': {
            'level': 'INFO',
            'handlers': ('console_handler',)
        },
        'err_logger': {
            'level': 'ERROR',
            'handlers': ('file_handler', 'console_handler')
        }
    }
}
