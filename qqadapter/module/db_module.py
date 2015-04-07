# -*- coding:utf8 -*-
__author__ = 'changyuf'

import MySQLdb
import logging
from qqadapter.bean.qquser import QQUser
from qqadapter.utilities.utilities import to_str


class DBModule:
    def __init__(self, host, user, password, data_base):
        self.host = host
        self.user = user
        self.password = password
        self.data_base = data_base
        self.db = MySQLdb.connect(host, user, password, data_base, charset='utf8', use_unicode=True)

    def insert_user(self, qq_user):
        cursor = self.db.cursor()
        sql = """INSERT INTO qq_account
                (uin, qq, nick_name, gender, balance,
                club_level, activity_times, accumulate_points, card, comments, other_comments)
            VALUES
                ("{user.uin}", "{user.qq}", "{user.nick_name}", "{user.gender}", {user.balance},
                {user.club_level}, {user.activity_times}, {user.accumulate_points}, "{user.card}", "{user.comments}", "{user.other_comments}");""".format(user=qq_user)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except:
            # Rollback in case there is any error
            logging.error("Insert user into database failed. SQL:%s", sql)
            self.db.rollback()

    def update_db_info(self, qq_user):
        logging.info("UIN Change: qq:%s, uin:%s", qq_user.qq, qq_user.uin)
        cursor = self.db.cursor()
        sql = "update qq_account set uin='%s', nick_name=%s, card='%s' where qq='%s'" % (qq_user.uin, qq_user.nick_name, qq_user.card, qq_user.qq)

        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except:
            # Rollback in case there is any error
            logging.error("update uin failed. SQL:%s", sql)
            self.db.rollback()

    def get_user(self, user):
        cursor = self.db.cursor()
        sql = """SELECT uin, qq, nick_name, gender, balance, club_level, activity_times, accumulate_points, card, comments, other_comments
            FROM qq_account WHERE qq = '%s'""" % user.qq
        users = []
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                #print row
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
        except:
            logging.error("get user from database failed. SQL:%s", sql)

        if len(users) == 0:
            return None
        return users[0]


if __name__ == '__main__':
    msg_patten = """
会员名：{user.nick_name}   性别：{user.gender}
会员级别：{user.club_level}
账户余额：{user.balance}
参加活动次数：{user.activity_times}
积分：{user.accumulate_points}
自我评价：{user.comments}
别人评价：{user.other_comments}"""
    module = DBModule("104.131.158.219", "changyuf", "changyuf", "club_robot")
    qq_user = QQUser()
    qq_user.uin = "123456"
    # qq_user.qq = "123456789"
    # qq_user.nick_name = "假人"
    # qq_user.gender = 'M'
    #values = '{user.uin},{user.qq},{user.nick_name}'.format(user=qq_user)
    users = module.get_user(qq_user)
    for qq_user in users:
        values = msg_patten.format(user=qq_user)
        print values


    #module.insert_user(qq_user)


