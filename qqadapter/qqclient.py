# -*- coding:utf8 -*-

__author__ = 'changyuf'

import requests
from qqadapter.core.qqsession import QQSession
from qqadapter.action.get_login_sig_action import GetLoginSigAction
from qqadapter.action.check_verify_action import CheckVerifyAction
from qqadapter.bean.qquser import QQAccount


class QQClient:
    def __init__(self, qq, password):
        self.account = QQAccount
        self.account.user_name = qq
        self.account.password = password

        self.session = QQSession
        # self.session = requests.Session()
        #self.session.headers.update(HEADERS)
        #self.client_id = None
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


    def __get_log_sig(self):
        return GetLoginSigAction.get_log_sig(self.session)

    def __check_verify(self):
        ret = CheckVerifyAction.check_verify(self.session, self.account.user_name)
        if ret[0]:
            return False



if __name__ == "__main__":
    client = QQClient('2899530487', '123456789')
    client.login()