# -*- coding:utf8 -*-
__author__ = 'changyuf'

import re
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
        if not qq_user.card:
            qq_user.card = qq_user.nick_name
        sql = "update qq_account set uin='%s', nick_name='%s', card='%s',gender='%s' where qq='%s'" % (qq_user.uin, qq_user.nick_name, qq_user.card, qq_user.gender, qq_user.qq)

        return self.db_manager.execute(sql)

    def update_user_comments(self, msg):
        qq_user = msg.from_user
        logging.info("Update comments: qq:%s", qq_user.qq)
        comments = msg.message
        comments = comments.replace(" ", "")
        comments = comments.replace("*自评", "")
        if len(comments) > 150:
            return "%s,你的自我评价太长，评价不能超过100个字" % qq_user.card

        sql = "update qq_account set comments='%s' where qq='%s'" % (comments, qq_user.qq)

        if self.db_manager.execute(sql):
            return "%s,自评成功" % qq_user.card
        else:
            return "%s,小秘书今天心情不好，你的自评失败" % qq_user.card

    def update_user_other_comments(self, msg):
        qq_user = msg.from_user
        logging.info("Update other comments: qq:%s", qq_user.qq)
        content = msg.message
        content = content.replace("*评价", "")
        content = content.strip()
        items = re.split(" +", content, 1)
        card = items[0]
        if len(items) > 1:
            comments = items[1]
        else:
            comments = ''

        if not card or not comments:
            return "%s,你的输入有误，不能评价" % qq_user.card

        if len(comments) > 150:
            return "%s,你的评价太长，评价不能超过100个字" % qq_user.card

        qqs = self.get_user_qq_by_card(card)
        if not qqs:
            return "%s,咱们俱乐部没有你输入的会员：'%s'" % (qq_user.card, card)

        sql = "update qq_account set other_comments='%s' where card='%s'" % (comments, card)

        if self.db_manager.execute(sql):
            return "%s,评价成功" % qq_user.card
        else:
            return "%s,小秘书今天心情不好，你的评价失败" % qq_user.card

    def get_user_qq_by_card(self, card):
        sql = """SELECT qq FROM qq_account WHERE card = '%s'""" % card
        qqs = []
        results = self.db_manager.fetchall(sql)

        for row in results:
            qqs.append(to_str(row[0]))

        return qqs

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

    def get_user_by_card(self, card):
        sql = """SELECT uin, qq, nick_name, gender, balance, club_level, activity_times, accumulate_points, card, comments, other_comments
            FROM qq_account WHERE card = '%s'""" % card
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

        return users

    def get_arrearage_user_message(self):
        sql = "SELECT card, balance FROM qq_account WHERE balance < 0"
        results = self.db_manager.fetchall(sql)
        if not results or len(results) == 0:
            return "没有欠费用户"

        content = "欠费用户：\\n"
        for row in results:
            content += "用户：%s, 欠费：%d\\n" % (to_str(row[0]), row[1])

        return content
