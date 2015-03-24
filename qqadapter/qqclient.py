# -*- coding:utf8 -*-

__author__ = 'changyuf'

import requests
from qqadapter.core.qqsession import QQSession
from qqadapter.action.get_login_sig_action import GetLoginSigAction
from qqadapter.action.check_verify_action import CheckVerifyAction
from qqadapter.bean.qquser import QQAccount
from qqadapter.utilities.utilities import HttpCookies
from qqadapter.action.web_login_action import WebLoginAction


class QQClient:
    def __init__(self, user_name, password):
        self.account = QQAccount(user_name, password)

        self.qq_session = QQSession
        self.verify_code = None
        self.uin = None
        # self.session = requests.Session()
        # self.session.headers.update(HEADERS)
        # self.client_id = None
        #self.session_id = None
        #self.vfwebqq = None
        #self.ptwebqq = None
        #self.qqStatus = "offline"
        #self.groupList = {}

    def login(self):
        if not self.__get_log_sig():
            print "get log_sig failed"
            return False

        if not self.__check_verify():
            print "check_verify failed"
            return False

        WebLoginAction.login(self.account, self.qq_session, self.verify_code)


    def __get_log_sig(self):
        return GetLoginSigAction.get_log_sig(self.qq_session)

    def __check_verify(self):
        ret = CheckVerifyAction.check_verify(self.qq_session, self.account.user_name)
        self.verify_code =  ret[1]
        self.uin = ret[2]
        if ret[0] == '1':
            return False

        return True


if __name__ == "__main__":
    client = QQClient('2899530487', '123456789')
    client.login()