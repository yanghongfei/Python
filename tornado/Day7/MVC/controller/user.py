#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/11 15:51
# @Author  : Fred Yang
# @File    : user.py
# @Role    : UserHandler， Class, 管理用户增删改查

from . import BaseHandler

import os, sys
import json
import tornado.web

Base_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(Base_DIR)
from MVC.model import orm
from MVC.utils.public import *

# 全局ORM对象
user_orm = orm.UserManagerORM()


class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')

        if not username or not password:
            return self.write(dict(status=-1, msg='用户密码不能为空'))

        if not user_orm.get_username(username):
            return self.write(dict(status=-10, msg='用户名不存在'))

        md5_password = md5_passwd(password)
        # print('password----->', md5_password)
        # print('1111----->',user_orm.get_user_password(username))

        if user_orm.get_user_password(username) == md5_password:
            self.set_secure_cookie('username', self.get_argument('username'))
            self.redirect('/')
        else:
            return self.write(dict(status=-10, msg='用户密码错误'))

class LogoutHandler(BaseHandler):
    def post(self):
        if (self.get_argument('logout', None)):
            self.clear_cookie('username')
        self.redirect('/')

class AddUserHandler(BaseHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        if user_orm.get_username(username):
            return self.write(dict(status=-1, msg="用户名:{} 已经存在".format(username)))

        password = self.get_argument('password')
        # 检测密码是否符合规范
        if not check_passwd(password):
            return self.write(dict(status=-2, msg='不符合密码规范，密码需要：超过10位，英文加数字，大小写'))

        # MD5加密写到数据库
        md5_password = md5_passwd(password)

        user_info = {
            "username": self.get_argument('username'),
            "age": self.get_argument('age'),
            "sex": self.get_argument('sex'),
            "score": self.get_argument('score'),
            "subject": self.get_argument('subject'),
            "password": md5_password,
        }

        user_orm.create_new_user(user_info)
        self.redirect('/')


class EditUserHandler(BaseHandler):
    def get(self, *args, **kwargs):
        user_info = user_orm.get_username(self.get_argument('username'))
        self.render('edit_user_info.html', user_info=user_info)

    def post(self, *args, **kwargs):
        pass


class UpdateUserInfoHandler(BaseHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        password = self.get_argument('password')
        # 检测密码是否符合规范
        if not check_passwd(password):
            return self.write(dict(status=-2, msg='不符合密码规范，密码需要：超过10位，英文加数字，大小写'))

        # MD5加密写到数据库
        md5_password = md5_passwd(password)
        user_info = {
            "username": self.get_argument('username'),
            "age": self.get_argument('age'),
            "sex": self.get_argument('sex'),
            "score": self.get_argument('score'),
            "subject": self.get_argument('subject'),
            "password": md5_password,
        }
        user_orm.update_username(user_info)
        self.redirect('/')


class DeleteUserHandler(BaseHandler):
    def get(self, *args, **kwargs):
        user_orm.delete_username(self.get_argument('username'))
        self.redirect('/')
