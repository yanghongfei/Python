#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/19 14:42
# @Author  : Fred Yang
# @File    : template.py
# @Role    : 说明脚本功能

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options

from tornado.options import define, options
from tornado.web import RequestHandler, url, StaticFileHandler
define("port", default=9000, help="run on the given port", type=int)


class IndexHandler(RequestHandler):
    def get(self):
        #定义的模板，可以随意修改
        houses = [
        {
            "price": 398,
            "title": "宽窄巷子+160平大空间+文化保护区双地铁",
            "score": 5,
            "comments": 6,
            "position": "北京市丰台区六里桥地铁"
        },
        {
            "price": 398123123,
            "title": "宽窄巷子+160平大空间+文化保护区双地铁",
            "score": 5,
            "comments": 6,
            "position": "北京市丰台区六里桥地铁"
        },
        {
            "price": 3923124248,
            "title": "宽窄巷子+160平大空间+文化保护区双地铁",
            "score": 5,
            "comments": 6,
            "position": "北京市丰台区六里桥地铁"
        },
        {
            "price": 3123213398,
            "title": "宽窄巷子+160平大空间+文化保护区双地铁",
            "score": 5,
            "comments": 6,
            "position": "北京市丰台区六里桥地铁"
        },
        {
            "price": 342142198,
            "title": "宽窄巷子+160平大空间+文化保护区双地铁",
            "score": 5,
            "comments": 6,
            "position": "北京市丰台区六里桥地铁"
        }]
        self.render("index.html", houses=houses)  # 渲染主页模板，并返回给客户端。

class NewHandler(RequestHandler):
    def get(self):
        self.render('new.html', text="")

    def post(self):
        text = self.get_argument("text", "")
        #print(text)
        self.render("new.html", text=text)


current_path = os.path.dirname(__file__)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        [
            (r'^/$', IndexHandler),
            (r'/add', NewHandler),
            (r'^/view/(.*)$', StaticFileHandler, {"path": os.path.join(current_path, "statics/html")}),
        ],
        static_path=os.path.join(current_path, "statics"),    #静态文件路径， 目录statics
        template_path=os.path.join(os.path.dirname(__file__), "templates"),  #模板路径，目录：templates
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


