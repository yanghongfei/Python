#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/11 15:48
# @Author  : Fred Yang
# @File    : __init__.py.py
# @Role    : base


import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('username')
