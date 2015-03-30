# -*- coding:utf8 -*-
__author__ = 'changyuf'

from enum import Enum
from qqadapter.bean.qquser import QQUser


class QQMessage:
    def __init__(self):
        self.id = 0  # 消息ID
        self.id2 = 0  # 暂时不知什么含义
        self.type = QQMessage.Type.BUDDY_MSG  # 消息类型
        self.to_user = None  # 消息发送方
        self.from_user = None  # 消息发送方
        self.group = None  # 所在群
        self.discuz = None  # 讨论组
        self.time = None  # 发送时间
        self.content_list = None  # 消息列表

    def dump(self):
        if self.id:
            print "id:", self.id
        if self.id2:
            print "id2:", self.id2
        if self.type:
            print "type:", self.type.name
        if self.to_user:
            print "to user:", self.to_user.nick_name
        if self.from_user:
            print "from user:", self.from_user.nick_name
        if self.group:
            print "from group:", self.group.name
        if self.content_list:
            print "content list:", self.content_list

    class Type(Enum):
        BUDDY_MSG = 0  # 好友消息
        GROUP_MSG = 1  # 群消息
        DISCUZ_MSG = 2  # 讨论组消息
        SESSION_MSG = 3  # 临时会话消息


if __name__ == '__main__':
    msg = QQMessage()
    msg.id = 1
    msg.id2 = 2
    msg.type = QQMessage.Type.BUDDY_MSG
    user1 = QQUser()
    user1.nick_name = "nick name 1"
    user2 = QQUser()
    user2.nick_name = "nick name 2"

    msg.to_user = user1
    msg.from_user = user2
    msg.content_list = "content list"
    msg.dump()
