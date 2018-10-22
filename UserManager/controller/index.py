#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/11 15:52
# @Author  : Fred Yang
# @File    : index.py
# @Role    : 首页url


from . import BaseHandler
from .user import user_orm

import tornado.web


class MainHandler(BaseHandler):
    """
    主Handler, 响应首页URL
    """

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        title = 'User Manager V0.1'  # 发送到user_manager.html中，标题
        users = user_orm.get_alluser()
        self.render('user_manager.html', title=title, users=users)
