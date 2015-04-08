# -*- coding:utf8 -*-
__author__ = 'changyuf'


class Activity:
    def __init__(self):
        self.id = 0
        self.title = ""
        self.description = ""
        self.activity_position = ""
        self.start_time = None
        self.stop_time = None
        self.price_male = 0
        self.price_female = 0
        self.max_participants = 0
        self.dead_line = None
        self.organiser = ""
        self.organiser_phone = ""

    def dump(self):
        print "ID：", self.id
        print "活动：", self.title
        print "描述：", self.description
        print "活动地点：", self.activity_position
        print "开始时间：", self.start_time
        print "结束时间：", self.stop_time
        print "费用男：", self.price_male
        print "费用女：", self.price_female
        print "最大人数：", self.max_participants
        print "报名截至时间：", self.dead_line
        print "组织者：", self.organiser
        print "组织者电话：", self.organiser_phone

