#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/10 10:57
# @Author  : Fred Yang
# @File    : cookies.py


import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('username')

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self, *args, **kwargs):
        self.set_secure_cookie('username', self.get_argument('username'))

        print('set--->',self.set_secure_cookie('username', self.get_argument('username')))

        self.redirect('/')

class WelcomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('index.html', user=self.current_user)


class LogoutHandler(BaseHandler):
    def get(self, *args, **kwargs):
        if (self.get_argument('logout', None)):
            self.clear_cookie('username')
            self.redirect('/')

    def post(BaseHandler):
        if (self.get_argument('logout', None)):
            self.clear_cookie('username')
            self.redirect('/')
if __name__ == '__main__':
    tornado.options.parse_command_line()

    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": True,
        "login_url": "/login"
    }

    application = tornado.web.Application([
        (r'/', WelcomeHandler),
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler)
    ], **settings)

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


