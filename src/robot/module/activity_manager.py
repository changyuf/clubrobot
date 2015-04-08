# -*- coding:utf8 -*-
__author__ = 'changyuf'

import datetime
from robot.utility.db_manager import DBManager
from robot.bean.activity import Activity
from robot.utility.utilities import to_str
from robot.module.participant_manager import ParticipantManager
from robot.utility.constants import Constants

# QUERY_ACTIVITY_REPLY_PATTEN = """{activity.title} {.gender}\\n会员级别：{user.club_level}\\n账户余额：{user.balance}\\n参加活动次数：{user.activity_times}\\n积分：{user.accumulate_points}\\n自我评价：{user.comments}\\n别人评价：{user.other_comments}"""


class ActivityManager:
    def __init__(self):
        self.db_manager = DBManager()
        self.participant_manager = ParticipantManager()

    def get_recent_activities(self):
        dt = datetime.datetime.now()
        begin_time = dt.strftime('%Y-%m-%d %H:%M:%S')
        dt2 = dt + datetime.timedelta(days=7)
        end_time = dt2.strftime('%Y-%m-%d %H:%M:%S')
        sql = """select id, title, activity_position,start_time,stop_time,price_male, price_female,
            max_participants,dead_line, organiser, organiser_phone from activities
            where start_time > '%s' and start_time < '%s'
            order by start_time""" % (begin_time, end_time)
        rows = self.db_manager.fetchall(sql)
        activities = []
        for row in rows:
            activity = Activity()
            activity.id = row[0]
            activity.title = to_str(row[1])
            activity.activity_position = to_str(row[2])
            activity.start_time = row[3]
            activity.stop_time = row[4]
            activity.price_male = row[5]
            activity.price_female = row[6]
            activity.max_participants = row[7]
            activity.dead_line = row[8]
            activity.organiser = to_str(row[9])
            activity.organiser_phone = to_str(row[10])

            activities.append(activity)

        return activities

    def get_query_activity_message(self, user):
        activities = self.get_recent_activities()
        #4月9日周四晚上7:00 后沙峪友瑞羽毛球俱乐部常规活动  0/12  杨峰  报名中
        text = "报名中的活动有：\\n"
        for activity in activities:
            text += "%s:  %s\\n" % (Constants.WEEKDAY[activity.start_time.weekday()], activity.title)
        return text


if __name__ == "__main__":
    manager = ActivityManager()
    activities = manager.get_recent_activities()
    for index, activity in enumerate(activities):
        print activity.start_time
        # activity_time = datetime.datetime.strptime(str(activity.start_time), '%Y-%m-%d %H:%M:%S')
        print "********* %s ***********" % Constants.WEEKDAY[activity.start_time.weekday()]
        activity.dump()