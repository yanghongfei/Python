#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/22 14:01
# @Author  : Fred Yang
# @File    : google_auth.py

import pyotp
import os
import sys
import fire

Base_DIR = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
sys.path.append(Base_DIR)

from qrcode import QRCode, constants
from UserManager.model import orm

auth_orm = orm.GoogleAuthORM()


class GoogleUserAuth():

    def create_user(self, username):
        secret_key = pyotp.random_base32()
        user_info = {
            'username': username,
            'secret_key': secret_key
        }
        auth_orm.create_user(user_info)

    def create_qrcode(self, username):
        """
        创建二维码，用于google auth扫码
        :param username: 用户名字
        :return:
        """
        '''二维码保存位置'''
        filepath = Base_DIR + '/static/google_auth/'
        # 根据username获取secert_key
        secret_key = auth_orm.get_user_secret_key(username)
        data = pyotp.totp.TOTP(secret_key).provisioning_uri(username, issuer_name='YangHongFeiTest')
        qr = QRCode(version=1, error_correction=constants.ERROR_CORRECT_L, box_size=6, border=4)
        try:
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image()
            print('QRCode Path:', filepath + username + '.png')
            img.save(filepath + username + '.png')
            return type
        except Exception as e:
            print(e)

    def google_verify_result(self, username, verifycode):
        """
        :param username: 用户
        :param verifycode: google auth上显示的动态口令
        :return:
            True： 验证通过
            False：验证失败
        """
        secret_key = auth_orm.get_user_secret_key(username)
        t = pyotp.TOTP(secret_key)
        result = t.verify(verifycode)  # 对输入验证码进行校验，正确返回True
        msg = result if result is True else False
        return msg


def main(username):
    """
    :param username: login username
    使用说明：python3 google_auth.py yanghongfei
    二维码地址：{project}/static/google_auth/{username}.png
    :return:
    """
    obj = GoogleUserAuth()
    obj.create_user(username)
    obj.create_qrcode(username)


if __name__ == '__main__':
    fire.Fire(main)
