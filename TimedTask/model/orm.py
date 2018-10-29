#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/24 17:03
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


class EventReminder():
    def __init__(self, name, content, email,advance_at,expire_at):
        """
        :param name: 提醒名字
        :param content: 提醒内容
        :param email: 提醒人员
        :param advance_at: 提前多少天提醒，int类型
        :param expire_at: 过期时间，到期时间等
        """
        self.name = name
        self.content = content
        self.email = email
        self.advance_at = advance_at
        self.expire_at = expire_at


class EventReminderORM():
    def __init__(self):
        self.engine = create_engine('mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(USER, PASSWD, HOST, PORT, DB_NAME))
        self.metadata = MetaData(self.engine)
        self.event_table = Table('event_reminder', self.metadata, autoload=True)
        # 将实体类User 映射到 User表
        mapper(EventReminder, self.event_table)
        # 生成一个会话类，并与上面建立的数据库引擎绑定
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

        self.session = self.Session()

    def get_all_event(self):
        """
        :return: 获取所有Event提醒
        """
        return self.session.query(EventReminder)

    def get_content(self, name):
        """
        获取一个名字
        :param content: 提醒内容
        :return:
        """
        return self.session.query(EventReminder).filter(EventReminder.name == name).first()

    def add_event(self, event_info):
        """
        添加Event提醒内容
        :param event_info: dict
        :return:
        """
        new_event = EventReminder(
            event_info['name'],
            event_info['content'],
            event_info['email'],
            event_info['advance_at'],
            event_info['expire_at'],
        )

        self.session.add(new_event)
        self.session.commit()
        self.session.close()

    def update_event(self, event_info):
        """
        根据·name·更新事件提醒内容
        :param event_info: dict
        :return:
        """
        name = event_info['name']
        event_info = {
            'content': event_info['content'],
            'email': event_info['email'],
            'advance_at': event_info['advance_at'],
            'expire_at': event_info['expire_at'],
        }
        self.session.query(EventReminder).filter(EventReminder.name == name).update(event_info)
        self.session.commit()
        self.session.close()

    def delete_event(self, name):
        self.session.query(EventReminder).filter(EventReminder.name == name).delete(synchronize_session=False)
        self.session.commit()
        self.session.close()
