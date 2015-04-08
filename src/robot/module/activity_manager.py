# -*- coding:utf8 -*-
__author__ = 'changyuf'

import datetime
import logging
from robot.utility.db_manager import DBManager
from robot.bean.activity import Activity
from robot.utility.utilities import to_str
from robot.module.participant_manager import ParticipantManager
from robot.bean.participant import Participant

#QUERY_ACTIVITY_REPLY_PATTEN = """{activity.title} {.gender}\\n会员级别：{user.club_level}\\n账户余额：{user.balance}\\n参加活动次数：{user.activity_times}\\n积分：{user.accumulate_points}\\n自我评价：{user.comments}\\n别人评价：{user.other_comments}"""


class WrongMessageException(Exception):
    pass


class ActivityManager:
    WEEKDAY = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    WEEKDAY_TO_INDEX = {"周一": 0, "周二": 1, "周三": 2, "周四": 3, "周五": 4, "周六": 5, "周日": 6}

    def __init__(self):
        self.db_manager = DBManager()
        self.participant_manager = ParticipantManager()

    def get_recent_activities(self):
        dt = datetime.datetime.now()
        begin_time = dt.strftime('%Y-%m-%d %H:%M:%S')
        dt2 = dt + datetime.timedelta(days=7)
        end_time = dt2.strftime('%Y-%m-%d %H:%M:%S')
        sql = """select title, activity_position,start_time,stop_time,price_male, price_female,
            max_participants,dead_line, organiser, organiser_phone from activities
            where start_time > '%s' and start_time < '%s'
            order by start_time""" % (begin_time, end_time)
        rows = self.db_manager.fetchall(sql)
        activities = []
        for row in rows:
            activity = Activity()
            activity.id = to_str(row[0])
            activity.title = to_str(row[1])
            activity.activity_position = to_str(row[2])
            activity.start_time = to_str(row[3])
            activity.stop_time = to_str(row[4])
            activity.price_male = int(row[5])
            activity.price_female = int(row[6])
            activity.max_participants = int(row[7])
            activity.dead_line = to_str(row[8])
            activity.organiser = to_str(row[9])
            activity.organiser_phone = to_str(row[10])

            activities.append(activity)

        return activities

    def get_query_activity_message(self, user):
        activities = self.get_recent_activities()
        #4月9日周四晚上7:00 后沙峪友瑞羽毛球俱乐部常规活动  0/12  杨峰  报名中
        text = "报名中的活动有：\\n"
        for activity in activities:
            text += "%s:  %s\\n" % (ActivityManager.WEEKDAY[activity.start_time.weekday()], activity.title)
        return text

    def enroll(self, msg):
        content = msg.message
        try:
            ret = ActivityManager.__parse_enroll_message(content)
        except WrongMessageException:
            logging.exception("ENROLL failed.")
            return "@%s,报名没成功，输入格式不正确" % msg.from_user.card

        activity = self.__get_activity(ret[0])
        if not activity:
            return "@%s,报名没成功，%s没有活动" % (msg.from_user.card, ActivityManager.WEEKDAY[ret[0]])

        dt = datetime.datetime.now()
        if dt > activity.dead_line:
            return "@%s,报名没成功，本次活动报名已经截至" % msg.from_user.card

        participants = self.participant_manager.get_participants(activity.id)
        number = ActivityManager.__get_participants_number(participants)
        if number == activity.max_participants:
            return "@%s,报名没成功，本次活动已经满员" % msg.from_user.card
        need_position = ret[1]["男"] + ret[1]["女"] + 1
        if number + need_position > activity.max_participants:
            return "@%s,本次活动的坑已经已经不够你报名%d人" % (msg.from_user.card, need_position)

        participant = ActivityManager.__construct_participant(msg.from_user, activity.id, ret[1])
        ret = self.participant_manager.insert_participant(participant)
        if not ret:
            return "@%s,小秘书心情不好，你本次报名没成功，请重试" % msg.from_user.card

        content = "%s  报名成功!\\n" % msg.from_user.card
        content += "活动：%s\\n" % activity.title
        content += "地点：【%s】\\n" % activity.activity_position
        content += "人数限制：%d/%d\\n" %(need_position, activity.max_participants)
        content += self.participant_manager.get_participant_message(activity.id)

        return content


    @staticmethod
    def __construct_participant(user, activity_id, add_on_dict):
        participant = Participant()
        participant.activity_id = activity_id
        participant.card = user.card
        participant.qq = user.qq
        participant.type = "QQ"
        participant.gender = user.gender
        participant.add_on_female = add_on_dict["女"]
        participant.add_on_male = add_on_dict["男"]

    @staticmethod
    def __get_participants_number(participants):
        number = 0
        for participant in participants:
            number += 1 + participant.add_on_male + participant.add_on_female

        return number



    def __get_activity(self, weekday):
        activities = self.get_recent_activities()
        for activity in activities:
            if weekday == activity.start_time.weekday():
                return activity

        return None

    @staticmethod
    def __parse_enroll_message(content):
        content = content.replace(" ", "")
        content = content.replace("#报名", "")
        if not content:
            raise WrongMessageException()
        its = content.split("+")
        num = len(its)
        activity_weekday = its[0]
        if activity_weekday not in ActivityManager.WEEKDAY_TO_INDEX.keys():
            raise WrongMessageException()
        weekday = ActivityManager.WEEKDAY_TO_INDEX[activity_weekday]
        add_on_dict = {"男": 0, "女": 0}
        if num > 1:
            ret = ActivityManager.__parse_add_on(its[1])
            add_on_dict[ret[0]] = ret[1]
        if num > 2:
            ret = ActivityManager.__parse_add_on(its[2])
            add_on_dict[ret[0]] = ret[1]

        return weekday, add_on_dict

    @staticmethod
    def __parse_add_on(text):
        if text[:2].isalnum():
            number = int(text[:2])
            gender = text[2:]
        elif text[:1].isalnum():
            number = int(text[:1])
            gender = text[1:]
        else:
            raise WrongMessageException()
        if gender != "男" and gender != "女":
            raise WrongMessageException()

        return gender, number


if __name__ == "__main__":
    text = "#报名 周二 + 1女 + 10男"

    try:
        ret = parse_message(text)
        activity_weekday = ret[0]
        add_on = ret[1]
        print activity_weekday
        print add_on
    except WrongMessageException, e:
        print "错误消息"

    exit()
    manager = ActivityManager()
    activities = manager.get_recent_activities()
    for index, activity in enumerate(activities):
        print activity.start_time
        #activity_time = datetime.datetime.strptime(str(activity.start_time), '%Y-%m-%d %H:%M:%S')
        print "********* %s ***********" % ActivityManager.WEEKDAY[activity.start_time.weekday()]
        activity.dump()

