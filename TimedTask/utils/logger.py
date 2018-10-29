#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/29 14:57
# @Author  : Fred Yang
# @File    : logger.py
# @Role    : 日志



import os
import logging
import shutil

def log(log_name='logger', file_folder='log',
        level=logging.INFO, delete_existed_logs=False):
    '''
    定义一个Log
    :param log_name: log 的名称
    :param file_folder: 保存的文件夹
    :param level: log 级别
    :param delete_existed_logs: 是否删除已有的log
    :return: 返回一个logger 对象
    '''

    if os.path.exists(file_folder):
        if delete_existed_logs:
            shutil.rmtree(file_folder)
            os.mkdir(file_folder)
    else:
        os.mkdir(file_folder)

    logger = logging.getLogger(log_name)
    logger.setLevel(level)
    file_handler = logging.FileHandler('%s/%s.log' % (file_folder, log_name), encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] - %(filename)s - [line:%(lineno)d] - [%(levelname)s]: %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger