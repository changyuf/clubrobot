# -*- coding:utf8 -*-

__author__ = 'changyuf'

import requests
import time
from qqadapter.core.qqsession import QQSession
from qqadapter.action.get_login_sig_action import GetLoginSigAction
from qqadapter.action.check_verify_action import CheckVerifyAction
from qqadapter.bean.qquser import QQAccount
from qqadapter.utilities.utilities import HttpCookies
from qqadapter.action.web_login_action import WebLoginAction
from qqadapter.action.get_captcha_image_action import GetCaptchaImageAction
from qqadapter.action.check_login_sig_action import CheckLoginSigAction


class QQClient:
    def __init__(self, user_name, password):
        self.account = QQAccount(user_name, password)

        self.qq_session = QQSession
        self.verify_code = None
        # self.uin = None
        # self.session = requests.Session()
        # self.session.headers.update(HEADERS)
        # self.client_id = None
        # self.session_id = None
        # self.vfwebqq = None
        #self.ptwebqq = None
        #self.qqStatus = "offline"
        #self.groupList = {}

    def login(self):
        if not self.__get_log_sig():
            print "get log_sig failed"
            return False

        need_input_verify_code = self.__check_verify()
        #web_login_ret = WebLoginAction.login(self.qq_session, self.account, self.verify_code, need_input_verify_code)

        if not need_input_verify_code:
            web_login_ret = WebLoginAction.login(self.qq_session, self.account, self.verify_code, False)
            # flag = True
            # while flag:
            #     web_login_ret = WebLoginAction.login(self.qq_session, self.account, self.verify_code, False)
            #     if web_login_ret[0] == '4': #页面过期，请重试
            #         print web_login_ret[2]
            #         time.sleep(5)
            #         web_login_ret = WebLoginAction.login(self.qq_session, self.account, self.verify_code, False)
            #     else:
            #         flag = False
        else:
            self.verify_code = self.__read_verify_code('为了保证您账号的安全，请输入验证码中字符继续登录')
            web_login_ret = WebLoginAction.login(self.qq_session, self.account, self.verify_code, True)
            # web_login_ret = ('4', 'url', '为了保证您账号的安全，请输入验证码中字符继续登录')
            # while web_login_ret[0] == '4':
            #     self.verify_code = self.__read_verify_code(web_login_ret[2])
            #     web_login_ret = WebLoginAction.login(self.qq_session, self.account, self.verify_code, True)

        while web_login_ret[0] == '4':
            self.verify_code = self.__read_verify_code(web_login_ret[2])
            web_login_ret = WebLoginAction.login(self.qq_session, self.account, self.verify_code, True)

        if not web_login_ret[0] == '0':
            return False

        CheckLoginSigAction.check_login_sig(web_login_ret[1])

    def __get_log_sig(self):
        return GetLoginSigAction.get_log_sig(self.qq_session)

    def __check_verify(self):
        ret = CheckVerifyAction.check_verify(self.qq_session, self.account.user_name)
        self.verify_code = ret[1]
        self.account.uin = ret[2]

        # test
        print "uin:"
        print self.account.uin

        if ret[0] == '1':
            return True
        return False


    def __read_verify_code(self, reason):
        GetCaptchaImageAction.get_captcha_image(self.account)
        return raw_input(reason + ":")


if __name__ == "__main__":
    client = QQClient('2899530487', '123456789')
    #client = QQClient('3106426008', 'leepet123')
    # 3047296752
    client.login()