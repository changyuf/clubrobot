# -*- coding:utf8 -*-
__metaclass__ = type
__author__ = 'changyuf'

from enum import Enum
import random


class QQUser:
    STATUS_DICT = {"online": 10, "offline": 20, "away": 30, "hidden": 40, "busy": 50, "callme": 60, "silent": 70}
    COMMENT_DICT = {
        0 : "本人很懒，不想写自我评价",
        1 : "本人智商不够，不会写自我评价",
        2 : "本人很NB，不屑于写自我评价",
        3 : "本人太平凡，怎么评价都行",
        4 : "一个字形容本人就是NB，两个字形容本人就是吹NB"
    }


    def __init__(self):
        self.uin_hex = None
        self.uin = None
        # fake_qq is qq in java
        self.qq = None
        self.status = None
        self.client_type = None  # 客户类型
        # private QQLevel level = None	#等级
        self.loginDate = None  # 登录时间
        self.nick_name = ''  # 昵称
        self.sign = None  # 个性签名
        self.gender = None  # 性别
        # the following field is used for qq robot
        self.balance = random.randint(1, 9999999)
        self.club_level = random.randint(0, 5)
        self.activity_times = 0
        self.accumulate_points = 0
        self.comments = self.COMMENT_DICT[random.randint(0, 4)]
        self.other_comments = "没有人愿意评价此人"
        #private Date birthday = None # 出生日期
        #self.phone = None # 电话
        #self.mobile = None # 手机
        #self.email = None # 邮箱
        #self.college = None # 毕业院校
        #private int regTime = None # 註冊時間
        #private int constel = None # 星座
        #private int blood = None # 血型
        #self.homepage = None # 个人主页
        #private int stat = None # 统计
        #private boolean isVip = None # 是否为VIP
        #private int vipLevel = None # VIP等级
        self.country = None  # 国家
        self.province = None  # 省
        self.city = None # 城市
        self.personal = None  # 个人说明
        #self.occupation  # 职业
        #private int chineseZodiac = None # 生肖
        #private int flag = None
        #private int cip = None
        #private transient BufferedImage face = None # 头像,不能被序列化
        #private QQAllow allow = None		#对方加好友验证请求设置

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
