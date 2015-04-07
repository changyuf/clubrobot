# -*- coding:utf8 -*-
__metaclass__ = type
__author__ = 'changyuf'

from qqadapter.bean.qq_stranger import QQStranger


class QQGroupMember(QQStranger):
    def __init__(self):
        super(QQGroupMember, self).__init__()
        self.group = None  # type isQQGroup
        self.card = ""

