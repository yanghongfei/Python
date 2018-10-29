#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/24 17:58
# @Author  : Fred Yang
# @File    : event.py
# @Role    : 事件提醒Handler


import os
import sys
import json
import tornado.web

Base_DIR = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
sys.path.append(Base_DIR)
from TimedTask.model import orm

# 全局ORM对象
event_orm = orm.EventReminderORM()


class EventHandler(tornado.web.RequestHandler):
    """事件路由 增删改查"""

    def get(self, *args, **kwargs):
        title = 'Event Manager v0.1'
        events = event_orm.get_all_event()
        self.render('event.html', title=title, events=events)

    def post(self, *args, **kwargs):
        '''新增一条事件'''
        data = json.loads(self.request.body.decode("utf-8"))

        name = data.get('name', None)
        content = data.get('content', None)
        email = data.get('email', None)
        advance_at = data.get('advance_at', None)
        expire_at = data.get('expire_at', None)

        if event_orm.get_content(name):
            return self.write(dict(status=-1, msg="name already exist..."))

        event_info = {
            "name": name,
            "content": content,
            "email": email,
            "advance_at": advance_at,
            "expire_at": expire_at,
        }

        event_orm.add_event(event_info)
        resp = {
            'status': 0,
            'msg': '添加成功'
        }
        return self.write(resp)

    def put(self, *args, **kwargs):
        '''更新信息'''
        data = json.loads(self.request.body.decode("utf-8"))
        name = data.get('name', None)
        content = data.get('content', None)
        email = data.get('email', None)
        advance_at = data.get('advance_at', None)
        expire_at = data.get('expire_at', None)

        event_info = {
            "name": name,
            "content": content,
            "email": email,
            "advance_at": advance_at,
            "expire_at": expire_at,
        }
        event_orm.update_event(event_info)
        resp = {
            'status': 0,
            'msg': '更新成功'
        }

        return self.write(resp)

    def delete(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        name = data.get('name', None)
        event_orm.delete_event(name)
        resp = {
            'status': 0,
            'msg': '删除成功'
        }
        return self.write(resp)



