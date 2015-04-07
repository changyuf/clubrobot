# -*- coding:utf8 -*-
__author__ = 'changyuf'

from qqadapter.core.qqsession import QQSession
from qqadapter.core.qqstore import QQStore
from qqadapter.bean.qquser import QQAccount
from qqadapter.utilities.http_service import HttpService


class QQContext:
    def __init__(self, user_name, password):
        self.account = QQAccount(user_name, password)
        self.qq_session = QQSession()
        self.http_service = HttpService()
        self.store = QQStore()


