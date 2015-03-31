# -*- coding:utf8 -*-
__author__ = 'changyuf'

import MySQLdb


class DBModule:
    def __init__(self, host, user, password, data_base):
        self.host = host
        self.user = user
        self.password = password
        self.data_base = data_base
        self.db = MySQLdb.connect(host, user, password, data_base, charset='utf8', use_unicode=True)

    def insert_user(self, user):
        cursor = self.db.cursor()
        # SQL 插入语句
        sql = """INSERT INTO qq_account
                (uin, qq, nick_name, gender, balance,
                level, activity_times, accumulate_points, comment, other_comment)
            VALUES
                ('3173831764', '3173831764', '牛逼人物', 'M', 2000,
                1, 0, 10, "很牛逼", "很中肯");"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except:
            # Rollback in case there is any error
            print "Insert failed"
            self.db.rollback()

    def get_user(self):
        cursor = self.db.cursor()

        # SQL 查询语句
        # sql = """SELECT (uin, qq, nick_name, gender, balance,
        #         level, activity_times, accumulate_points, comment, other_comment) FROM qq_account
        #        WHERE uin == '%s'""" % "3173831764"
        sql = "select * from qq_account"
        try:
            # 执行SQL语句
            cursor.execute(sql)
            print "after execute sql"
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                #print row
                for data in row:
                    if isinstance(data, unicode):
                        data = data.encode('utf8')
                    print data
                # fname = row[0]
                # lname = row[1]
                # age = row[2]
                # sex = row[3]
                # income = row[4]
                # # 打印结果
                # print "fname=%s,lname=%s,age=%d,sex=%s,income=%d" % \
                # (fname, lname, age, sex, income )
        except:
            print "Error: unable to fetch data"


if __name__ == '__main__':
    module = DBModule("104.131.158.219", "changyuf", "changyuf", "club_robot")
    module.insert_user(None)
    module.get_user()
