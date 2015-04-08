# -*- coding:utf8 -*-
__author__ = 'changyuf'

import logging
from robot.utility.utilities import to_str
from qqadapter.bean.qquser import QQUser
from robot.utility.db_manager import DBManager

class QQAccountManager:
    def __init__(self):
        self.db_manager = DBManager()

    def insert_user(self, qq_user):
        sql = """INSERT INTO qq_account
                (uin, qq, nick_name, gender, balance,
                club_level, activity_times, accumulate_points, card, comments, other_comments)
            VALUES
                ("{user.uin}", "{user.qq}", "{user.nick_name}", "{user.gender}", {user.balance},
                {user.club_level}, {user.activity_times}, {user.accumulate_points}, "{user.card}", "{user.comments}", "{user.other_comments}");""".format(user=qq_user)
        return self.db_manager.execute(sql)

    def update_db_info(self, qq_user):
        logging.info("UIN Change: qq:%s, uin:%s", qq_user.qq, qq_user.uin)
        sql = "update qq_account set uin='%s', nick_name='%s', card='%s' where qq='%s'" % (qq_user.uin, qq_user.nick_name, qq_user.card, qq_user.qq)

        return self.db_manager.execute(sql)

    def get_user(self, user):
        sql = """SELECT uin, qq, nick_name, gender, balance, club_level, activity_times, accumulate_points, card, comments, other_comments
            FROM qq_account WHERE qq = '%s'""" % user.qq
        users = []
        results = self.db_manager.fetchall(sql)

        for row in results:
            user = QQUser()
            user.uin = to_str(row[0])
            user.qq = to_str(row[1])
            user.nick_name = to_str(row[2])
            user.gender = to_str(row[3])
            user.balance = row[4]
            user.club_level = row[5]
            user.activity_times = row[6]
            user.accumulate_points = row[7]
            user.card = to_str(row[8])
            user.comments = to_str(row[9])
            user.other_comments = to_str(row[10])
            users.append(user)

        if len(users) == 0:
            return None
        return users[0]
