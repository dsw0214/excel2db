# -*- coding: utf-8 -*-
# @Time    : 2019/1/27 下午4:09
# @Author  : shiwei-Du
# @Email   : dusw0214@126.com
# @File    : Log.py
# @Software: PyCharm

import logging
import logging.config
from os import path


class Log():
    def __init__(self):
        log_file_path = path.join(path.dirname(path.abspath(__file__)), '../config/logging.conf')
        logging.config.fileConfig(log_file_path)
        self.logger = logging.getLogger(name='rotatingFileLogger')

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def warning(self, msg):
        self.logger.warning(msg)