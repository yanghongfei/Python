#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/12 15:18
# @Author  : Fred Yang
# @File    : public.py
# @Role    : 公共工具


import re
import hashlib


def check_passwd(data):
    return True if re.search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$", data) and len(data) >= 10 else False


def md5_passwd(data):
    md5 = hashlib.md5()
    md5.update(bytes(data, encoding='utf-8'))
    password = md5.hexdigest()
    return password
