# -*- coding:utf8 -*-
__author__ = 'changyuf'


class QQGroup:
    def __init__(self):
        self.gid = None  # 真实的群号
        self.gin = None  # 变换后的群号
        self.code = None
        self.clazz = None
        self.flag = None
        self.level = None
        self.mask = None
        self.name = None
        self.memo = None
        self.fingermemo = None
        self.createTime = None
        self.face = None  # 头像
        self.members = []  # QQGroupMember list

    def __str__(self):
        return str({
            'gid': self.gid,
            'gin': self.gin,
        })


if __name__ == '__main__':
    group = QQGroup()
    group.gid = "12345"