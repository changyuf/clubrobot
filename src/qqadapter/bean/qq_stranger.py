# -*- coding:utf8 -*-
__metaclass__ = type
__author__ = 'changyuf'

from qqadapter.bean.qquser import QQUser

class QQStranger(QQUser):
    def __init__(self):
        super(QQStranger, self).__init__()
        self.group_sig = None
        self.service_type = -1
        self.token = ""

