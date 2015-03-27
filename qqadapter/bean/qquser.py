# -*- coding:utf8 -*-
__metaclass__ = type
__author__ = 'changyuf'

from enum import Enum


class QQUser:
    STATUS_DICT = {"online": 10, "offline": 20, "away": 30, "hidden": 40, "busy": 50, "callme": 60, "silent": 70}

    def __init__(self):
        self.uin_hex = None
        self.uin = None
        # fake_qq is qq in java
        self.qq = None
        status = None
        #private QQClientType clientType = None # 客户类型
        #private QQLevel level = None	#等级
        self.loginDate = None  # 登录时间
        self.nickname = None  # 昵称
        self.sign = None  # 个性签名
        self.gender = None  # 性别
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
        #self.country = None # 国家
        #self.province = None # 省
        #self.city = None # 城市
        self.personal = None  # 个人说明
        #self.occupation  # 职业
        #private int chineseZodiac = None # 生肖
        #private int flag = None
        #private int cip = None
        #private transient BufferedImage face = None # 头像,不能被序列化
        #private QQAllow allow = None		#对方加好友验证请求设置


class QQAccount(QQUser):
    def __init__(self, user_name, password):
        super(QQAccount, self).__init__()
        self.password = password
        self.user_name = user_name
