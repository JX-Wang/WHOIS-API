#! /usr/bin/env python
# coding:utf-8
"""
日志模块 log.py
==============
author  :   wud
date    :   2018.8.21
ver     :   0.1
"""

import logging.config
import time
import os


class Log(object):
    """log method"""
    _init_done = True

    def __getstate__(self):
        return self.__dict__

    def __init__(self):
        """initial"""
        pass
        '''
        self.logfile = "running.log"
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        rq = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # log_path = os.path.dirname(os.getcwd()) + log_name
        log_name = "running" + rq + ".log"
        logfile = log_name
        fh = logging.FileHandler(logfile, mode='w')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        '''

    logger = None
    LOG_CONF = None

    @staticmethod
    def init():
        try:
            now_path = os.path.abspath('.')
            # print now_path
            logger_path = now_path + "/Log/logger.conf"
            # print logger_path
            logging.config.fileConfig(logger_path)
        except Exception as e:
            print "fileConfig Error - >", str(e)
            exit(0)
        Log.logger = logging.getLogger('main')
        '''
        Log.logger.debug('什么意思？')
        Log.logger.info('为什么不能记录')
        Log.logger.warn('》}》？P》“？&%……*@#@')
        Log.logger.error('奇了怪了？？？！！！')
        Log.logger.critical(int(127391731))
        '''
        # log = Log.logger

    '''
    def debug(self, debug):
        """log debug"""
        self.logger.debug(debug)

    def info(self, info):
        """log info"""
        self.logger.info(info)

    def warning(self, warning):
        """log warning"""
        self.logger.warning(warning)

    def error(self, error):
        """log error"""
        self.logger.error(error)

    def critical(self, critical):
        """log critical"""
        self.logger.critical(critical)
    '''


if __name__ == '__main__':
    '''
    log = Log()
    log.error("this is a error log")
    log.warning("this is a warning log")
    log.info("this is a info log")
    log.debug("this is a debug log")
    log.critical("this is a critical log")
    '''
    Log.init()
    log = Log.logger
    log.debug('什么意思？')
    log.info('为什么不能记录')
    log.warn('》}》？P》“？&%……*@#@')
    log.error('奇了怪了？？？！！！')
    log.critical(int(127391731))



