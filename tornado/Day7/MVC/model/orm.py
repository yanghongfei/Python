#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/11 11:03
# @Author  : Fred Yang
# @File    : orm.py


from sqlalchemy import *
from sqlalchemy.orm import *

import sys, os

Base_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(Base_DIR)

from settings import DB_INFO

HOST = DB_INFO['host']
USER = DB_INFO['user']
PORT = DB_INFO['port']
PASSWD = DB_INFO['password']
DB_NAME = DB_INFO['db_name']


class User():
    def __init__(self, username, age, sex, score, subject, password):
        self.username = username
        self.age = age
        self.sex = sex
        self.score = score
        self.subject = subject
        self.password = password


class UserManagerORM():
    def __init__(self):
        self.engine = create_engine('mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(USER, PASSWD, HOST, PORT, DB_NAME))
        self.metadata = MetaData(self.engine)
        self.user_table = Table('user', self.metadata, autoload=True)
        # 将实体类User 映射到 User表
        mapper(User, self.user_table)
        # 生成一个会话类，并与上面建立的数据库引擎绑定
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

        self.session = self.Session()

    def create_new_user(self, user_info):
        """
        新建用户
        :param user_info:  列表
        :return:
        """

        new_user = User(
            user_info['username'],
            user_info['age'],
            user_info['sex'],
            user_info['score'],
            user_info['subject'],
            user_info['password'],
        )
        self.session.add(new_user)
        self.session.commit()
        self.session.close()

    def get_username(self, username):
        """
        :param username: 根据用户名返回信息
        :return:
        """
        return self.session.query(User).filter(User.username == username).first()

    def get_user_password(self, username):
        """
        :param username: 根据用户名返回密码
        :return:
        """
        res = self.session.query(User).filter(User.username == username).first()
        return res.password

    def get_alluser(self):
        """
        :return:  获取所有用户信息
        """
        return self.session.query(User)

    def update_username(self, user_info):
        """
        根据用户名字修改用户信息
        :param user_info:
        :return:
        """
        username = user_info['username']
        username_info = {
            'age': user_info['age'],
            'sex': user_info['sex'],
            'score': user_info['score'],
            'subject': user_info['subject'],
            "password": user_info['password']
        }

        self.session.query(User).filter(User.username == username).update(username_info)
        self.session.commit()
        self.session.close()

    def delete_username(self, username):
        self.session.query(User).filter(User.username == username).delete(synchronize_session=False)
        self.session.commit()
        self.session.close()
