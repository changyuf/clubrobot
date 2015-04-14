# -*- coding:utf8 -*-
__metaclass__ = type
__author__ = 'changyuf'

from enum import Enum
import random


class QQUser:
    STATUS_DICT = {"online": 10, "offline": 20, "away": 30, "hidden": 40, "busy": 50, "callme": 60, "silent": 70}
    COMMENT_DICT = {
        0: "本人很懒，不想写自我评价",
        1: "本人智商不够，不会写自我评价",
        2: "本人很NB，不屑于写自我评价",
        3: "本人太平凡，怎么评价都行",
        4: "一个字形容本人就是NB，两个字形容本人就是吹NB"
    }

    def __init__(self):
        self.uin_hex = None
        self.uin = None
        self.qq = None
        self.status = None
        self.client_type = None  # 客户类型
        self.loginDate = None  # 登录时间
        self.nick_name = ''  # 昵称
        self.sign = None  # 个性签名
        self.gender = None  # 性别
        self.card = ""
        self.country = None  # 国家
        self.province = None  # 省
        self.city = None  # 城市
        self.personal = None  # 个人说明
        # the following field is used for qq robot
        self.balance = 0  # random.randint(1, 100)
        self.club_level = random.randint(0, 5)
        self.activity_times = 0
        self.accumulate_points = 0
        # self.comments = self.COMMENT_DICT[random.randint(0, 4)]
        self.comments = ""
        # self.other_comments = "没有人愿意评价此人"
        self.other_comments = ""

    class Status(Enum):
        ONLINE = 10
        OFFLINE = 20
        AWAY = 30
        HIDDEN = 40
        BUSY = 50
        CALLME = 60
        SILENT = 70


class QQAccount(QQUser):
    def __init__(self, user_name, password):
        super(QQAccount, self).__init__()
        self.password = password
        self.user_name = user_name
