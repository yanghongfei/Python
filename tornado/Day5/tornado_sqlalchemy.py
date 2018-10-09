#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/30 10:49
# @Author  : Fred Yang
# @File    : tornado_sqlalchemy.py
# @Role    : Sqlalchemy 增删改查



# 导入
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import DB_INFO

HOST=DB_INFO['host']
USER=DB_INFO['user']
PORT=DB_INFO['port']
PASSWD=DB_INFO['password']
DB_NAME= DB_INFO['db_name']

# 创建对象的基类:
Base = declarative_base()

#定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(String(100), primary_key=True)
    name = Column(String(200))

class Weibo(Base):
    __tablename__ = 'weibo'
    id = Column(String(100), primary_key=True)
    username = Column(String(100))  #用户名
    content = Column(String(1000)) #内容

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(USER, PASSWD, HOST, PORT, DB_NAME))


#print(engine)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

Base.metadata.create_all(engine)  #创建表的语句 第一次使用


