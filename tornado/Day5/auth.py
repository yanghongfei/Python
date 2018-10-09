#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/8 10:25
# @Author  : Fred Yang
# @File    : user_login.py
# @Role    : 提交内容到数据库里面


import os.path
import time
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import tornado.escape
from tornado.options import define, options
from tornado_sqlalchemy import DBSession
from tornado_sqlalchemy import Weibo

define("port", default=8000, help='run server port', type=int)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class WeiboHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('weibo_add.html')

    @tornado.web.authenticated

    def post(self, *args, **kwargs):
        # data = json.loads(self.request.body.decode("utf-8"))
        content = self.get_argument("content", None)
        username = self.get_secure_cookie("user")
        session = DBSession()
        name_info = session.query(Weibo).filter(Weibo.content == content).first()

        if name_info:
            return self.write(dict(status=-3, msg='内容已存在'))

        else:
            session = DBSession()
            session.add(Weibo(id=time.time(),username=username, content=content))
            session.commit()
            session.close()


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)
        #self.write('Hello, User:'+ self.current_user)


class LoginHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

    def post(self, *args, **kwargs):
        self.set_secure_cookie('user', self.get_argument('name'))
        self.redirect('/')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/login', LoginHandler),
            (r'/weibo/add', WeiboHandler),
        ]
        settings = dict(
            cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/login",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            debug=True,
        )
        tornado.web.Application.__init__(self,handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()

