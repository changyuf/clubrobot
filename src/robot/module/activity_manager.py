# -*- coding:utf8 -*-
__author__ = 'changyuf'

import datetime
from robot.utility.db_manager import DBManager
from robot.bean.activity import Activity
from robot.utility.utilities import to_str


class ActivityManager:
    def __init__(self):
        self.db_manager = DBManager()

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
            activity.title = to_str(row[0])
            activity.activity_position = to_str(row[1])
            activity.start_time = to_str(row[2])
            activity.stop_time = to_str(row[3])
            activity.price_male = int(row[4])
            activity.price_female = int(row[5])
            activity.max_participants = int(row[6])
            activity.dead_line = to_str(row[7])
            activity.organiser = to_str(row[8])
            activity.organiser_phone = to_str(row[9])

            activities.append(activity)

        return activities


if __name__ == "__main__":
    weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日", ]
    manager = ActivityManager()
    activities = manager.get_recent_activities()
    for index, activity in enumerate(activities):
        print activity.start_time
        #activity_time = datetime.datetime.strptime(str(activity.start_time), '%Y-%m-%d %H:%M:%S')
        print "********* %s ***********" % weekday[activity.start_time.weekday()]
        activity.dump()

