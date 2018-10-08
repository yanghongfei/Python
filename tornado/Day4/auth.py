 #!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/8 10:25
# @Author  : Fred Yang
# @File    : auth.py


import os.path
import json
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import tornado.escape
from tornado.options import define, options

define("port", default=8000, help='run server port', type=int)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")



class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)
    # def get(self):
    #     if not self.current_user:
    #         self.redirect("/login")
    #         return
    #     name = tornado.escape.xhtml_escape(self.current_user)
    #     self.write("Hello," + name )


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
        ]
        settings = dict(
            cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/login",
        )
        tornado.web.Application.__init__(self,handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()

