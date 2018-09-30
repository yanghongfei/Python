#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/30 14:23
# @Author  : Fred Yang
# @File    : app.py

import os.path
import json
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import define, options
from tornado_sqlalchemy import DBSession
from tornado_sqlalchemy import User

define("port", default=8000, help='run server port', type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<h1>tornado_sqlalchemy index</h1><br></br><h2>可以使用get/put/post/delete进行增删改查</h2>')

class UserHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        user_id = self.get_argument('user_id', default=1, strip=True)
        print(user_id)
        if user_id:
            session = DBSession()
            user = session.query(User).filter(User.id == user_id).one()
            session.close()
            # print('type:', type(user))
            #print('name:', user.name)
            self.write('你user_id对应的name是：{}'.format(user.name))

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        #print(data)
        user_id = data.get('id', None)
        username = data.get('name', None)
        # print(user_id,username)
        # print(bool(user_id))
        # print(bool(username))

        if not username or not user_id:
            return self.write(dict(status=-1, msg='参数不能为空'))

        session = DBSession()
        name_id = session.query(User).filter(User.id == user_id).first()
        name_info = session.query(User).filter(User.name == username).first()
        if name_id:
            return self.write(dict(status=-2, msg='用户ID已存在'))

        if name_info:
            return self.write(dict(status=-3, msg='用户名字已存在'))

        else:
            session = DBSession()
            session.add(User(id=user_id, name=username))
            session.commit()
            session.close()
            self.write(dict(status=0, msg='用户：{}创建成功'.format(username)))

    def put(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        user_id = data.get('id', None)
        username = data.get('name', None)

        if not username or not user_id:
            return self.write(dict(status=-1, msg='参数不能为空'))

        session = DBSession()
        session.query(User).filter(User.id == user_id).update({User.name: username})  #指定的IP更改username
        session.commit()
        session.close()
        return self.write(dict(status=0, msg='更新成功'))

    def delete(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        #user_id = data.get('id', None)
        username = data.get('name', None)

        if not username:
            return self.write(dict(status=-1, msg='参数不能为空'))

        session = DBSession()
        session.query(User).filter(User.name == username).delete(synchronize_session=False)
        session.commit()
        session.close()
        return self.write(dict(status=0, msg='用户：{} 删除成功'.format(username)))





class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/users', UserHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
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
