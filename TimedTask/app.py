#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/24 17:00
# @Author  : Fred Yang
# @File    : app.py
# @Role    : 事件提醒

import os.path
import sys
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
from tornado.options import define, options
Base_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(Base_DIR)

# 不同类型的Jamd;er进行了拆分维护，app.py只作为server入口
from TimedTask.controller.event import EventHandler

define("port", default=8888, help='run on the given port', type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/event', EventHandler)
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            # cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            # xsrf_cookies=True,
            # login_url="/login",
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
