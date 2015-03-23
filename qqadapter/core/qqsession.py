# -*- coding:utf8 -*-

__author__ = 'changyuf'


class QQSession:
    def __init__(self):
        self.session_id = None
        self.vfwebqq = None
        self.ptwebqq = None
        self.login_sig = None
        self.cface_key = None  # 上传群图片时需要
        self.cface_sig = None  # 上传群图片时需要
        self.email_auth_key = None  # 邮箱登录认证
        self.index = None  # 禁用群时需要
        self.port = None  # 禁用群时需要
        self.pollErrorCnt = None
        self.state = QQSession.State.OFFLINE

    class State:
        (OFFLINE, ONLINE, KICKED, LOGINING, ERROR) = range(0, 5)