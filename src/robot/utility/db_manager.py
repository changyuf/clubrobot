# -*- coding:utf8 -*-
__author__ = 'changyuf'
import MySQLdb
import datetime
import logging
from robot.utility.singleton import Singleton
from robot.utility.config import Config
from qqadapter.utilities.utilities import to_str


class DBManager(Singleton):
    def __init__(self):
        self.config = Config()
        self.host = self.config.get("db", "db_host")
        self.user = self.config.get("db", "db_user")
        self.password = self.config.get("db", "db_pass")
        self.data_base = self.config.get("db", "data_base")

    def fetchall(self, sql):
        try:
            con = db = MySQLdb.connect(self.host, self.user, self.password, self.data_base, charset='utf8', use_unicode=True)
            cur = con.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
        except MySQLdb.Error, e:
            logging.error("fetch data from database failed. SQL:%s", sql)
            logging.error("Error %d: %s", e.args[0], e.args[1])
            logging.exception("fetchh data from databse failed")
        finally:
            if con:
                con.close()

        return rows

    def execute(self, sql):
        try:
            con = db = MySQLdb.connect(self.host, self.user, self.password, self.data_base, charset='utf8', use_unicode=True)
            cur = con.cursor()
            cur.execute(sql)
            con.commit()
        except MySQLdb.Error, e:
            if con:
                con.rollback()
            logging.error("fetch data from database failed. SQL:%s", sql)
            logging.error("Error %d: %s", e.args[0], e.args[1])
            logging.exception("fetch data from database failed")
            return False
        finally:
            if con:
                con.close()

        return True

if __name__ == "__main__":
    db = DBManager()
    dt = datetime.datetime.now()
    begin_time = dt.strftime('%Y-%m-%d %H:%M:%S')
    dt2 = dt + datetime.timedelta(days=7)
    end_time = dt2.strftime('%Y-%m-%d %H:%M:%S')
    sql = """select title, activity_position,start_time,stop_time,cost_male, cost_female,
        max_participants,dead_line, organiser, organiser_phone from activities
        where start_time > '%s' and start_time < '%s'""" % (begin_time, end_time)
    rows = db.fetchall(sql)
    for row in rows:
        for col in row:
            print to_str(col)
        print "***************"

