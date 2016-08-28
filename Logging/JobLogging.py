#-*- coding:utf-8 -*-
import logging
import time

class JobLogging:
    """log module"""
    def __init__(self, task_name, log_path):
        self.logger = logging.getLogger(task_name)
        self.level = 'DEBUG'
        self.logger.setLevel(logging.DEBUG)
        self.consoleHandler = logging.StreamHandler()
        self.consoleHandler.setLevel(logging.DEBUG)
        self.fileHandler = logging.FileHandler(filename=log_path + '/' + task_name + '.' + time.strftime('%Y%m%d') + '.log', mode='a', encoding='utf8')
        self.fileHandler.setLevel(logging.DEBUG)
        loggerFormatter = logging.Formatter('%(asctime)s [%(lineno)s] %(levelname)s %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')
        self.consoleHandler.setFormatter(loggerFormatter)
        self.fileHandler.setFormatter(loggerFormatter)

    def get_logger(self):
        if self.level == 'DEBUG':
            self.logger.addHandler(self.consoleHandler)
            self.logger.addHandler(self.fileHandler)
        elif self.level == 'INFO':
            self.logger.addHandler(self.consoleHandler)
            self.logger.addHandler(self.fileHandler)
        else:
            self.logger.addHandler(self.consoleHandler)
            self.logger.addHandler(self.fileHandler)
        return self.logger

    def set_level(self, level):
        self.level = level
        if self.level == 'DEBUG':
            self.consoleHandler.setLevel(logging.DEBUG)
            self.fileHandler.setLevel(logging.DEBUG)
        elif self.level == 'INFO':
            self.consoleHandler.setLevel(logging.INFO)
            self.fileHandler.setLevel(logging.INFO)
        else:
            self.consoleHandler.setLevel(logging.DEBUG)
            self.fileHandler.setLevel(logging.DEBUG)

if __name__ == '__main__':
    myLog = JobLogging.etl_logging('mytest', '/home/sunnyin/study/python/Scripts/DouBan/logs')
#    myLog.set_level('INFO')
    myLogger = myLog.get_logger()
    myLogger.info('info')
    myLogger.debug('debug')

