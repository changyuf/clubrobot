# -*- coding:utf8 -*-
__author__ = 'changyuf'

from robot.utility.db_manager import DBManager
from robot.bean.bill_details import BillDetails
from robot.utility.utilities import to_str


class BillDetailsManager:
    def __init__(self):
        self.db_manager = DBManager()

    def get_bill_details(self, user_id):
        sql = """SELECT account_type, account_id, account_name, operator, operate_time, balance_change, balance, comments
                FROM account_bill_details
                WHERE account_id = '%s'
                ORDER BY operate_time DESC LIMIT 5""" % user_id

        rows = self.db_manager.fetchall(sql)
        bills = []
        for row in rows:
            bill = BillDetails()
            bill.account_type = to_str(row[0])
            bill.account_id = to_str(row[1])
            bill.account_name = to_str(row[2])
            bill.operator = to_str(row[3])
            bill.operate_time = row[4]
            bill.balance_change = row[5]
            bill.balance = to_str(row[6])
            bill.comments = to_str(row[7])
            bills.append(bill)

        return bills

    def get_bill_details_message(self, user):
        bills = self.get_bill_details(user.qq)
        if len(bills) == 0:
            return "@%s 您最近没有余额变更记录" % user.card

        content = "@%s 余额变更信息：\\n"
        for bill in bills:
            if not bill.comments:
                bill.comments = " "
            content += "%s, %d, %d, %s\\n" % (bill.operate_time.strftime('%Y-%m-%d %H:%M'), bill.balance_change, bill.balance, bill.comments)

        return content

    def get_accumulate_points_details_message(self, user):
        sql = """SELECT operate_time, points_change, points, comments
                FROM accumulate_points_details
                WHERE account_id = '%s'
                ORDER BY operate_time DESC LIMIT 10""" % user.qq

        rows = self.db_manager.fetchall(sql)
        if not rows or len(rows) == 0:
            return "@%s 您最近没有积分变更记录" % user.card

        content = "@%s 积分变更信息：\\n"
        for row in rows:
            if not row[3]:
                row[3] = " "
            content += "%s, %d, %d, %s" % ( row[0].strftime('%Y-%m-%d %H:%M'), row[1], row[2], row[3])

        return content
