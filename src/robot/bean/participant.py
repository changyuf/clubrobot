# -*- coding:utf8 -*-
__author__ = 'changyuf'


class Participant:
    def __init__(self):
        self.activity_id = 0
        self.card = ""
        self.qq = ""
        self.type = ""
        self.gender = ""
        self.add_on_female = 0
        self.add_on_male = 0

    def dump(self):
        print "活动ID：", self.activity_id
        print "群名片：", self.card
        print "QQ号：", self.qq
        print "报名类型：", self.type
        print "性别：", self.gender
        print "外挂女：", self.add_on_female
        print "外挂男：", self.add_on_male
