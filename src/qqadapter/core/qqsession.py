# -*- coding:utf8 -*-
__author__ = 'changyuf'

from enum import Enum


class QQSession(object):
    def __init__(self):
        self.client_id = None
        self.session_id = ""
        self.vfwebqq = None
        self.ptwebqq = None
        #self.login_sig = None
        self.cface_key = None  # 上传群图片时需要
        self.cface_sig = None  # 上传群图片时需要
        self.email_auth_key = None  # 邮箱登录认证
        self.index = None  # 禁用群时需要
        self.port = None  # 禁用群时需要
        self.pollErrorCnt = None
        self.__state = QQSession.State.OFFLINE

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        if isinstance(value, QQSession.State):
            self.__state = value
        else:
            print "invalid value for state"

    @state.deleter
    def state(self):
        del self.__state

    class State(Enum):
        (OFFLINE, ONLINE, KICKED, LOGINING, ERROR) = range(0, 5)