# -*- coding:utf8 -*-
__author__ = 'changyuf'

import logging
from qqadapter.bean.qq_message import QQMessage
from robot.module.activity_manager import ActivityManager
from robot.module.enroll_manager import EnrollManager
from robot.utility.config import Config
from robot.module.bill_details_manager import BillDetailsManager

QUERY_ACCOUNT_REPLY_PATTEN = """会员名：{user.card}   性别：{user.gender}\\n会员级别：{user.club_level}\\n账户余额：{user.balance}\\n参加活动次数：{user.activity_times}\\n积分：{user.accumulate_points}\\n自我评价：{user.comments}\\n别人评价：{user.other_comments}"""

class MessageProcessor:
    def __init__(self, chat_module, qq_account_manager):
        self.chat_module = chat_module
        self.qq_account_manager = qq_account_manager
        self.activity_manager = ActivityManager()
        self.enroll_manager = EnrollManager(self.activity_manager)
        self.config = Config()
        self.bill_details_manager = BillDetailsManager()

    def process(self, msg):
        if msg.type == QQMessage.Type.GROUP_MSG:
            self.__process_group_message(msg)

    def __process_group_message(self, msg):
        group_name = msg.group.name
        #if group_name == "运动测试" or group_name == "后沙峪友瑞羽毛球群":
        if group_name == self.config.get("robot", "group_name"):
            if msg.message.startswith("*小秘书"):
                self.__deal_with_call_me(msg)
            elif msg.message.startswith("*查询"):
                self.__deal_with_query_account(msg)
            elif msg.message.startswith("*活动"):
                self.__deal_with_query_activities(msg)
            elif msg.message.startswith("*报名"):
                self.__deal_with_enroll(msg)
            elif msg.message.startswith("*取消"):
                self.__deal_with_cancel_enroll(msg)
            elif msg.message.startswith("*周"):
                self.__deal_with_query_activity(msg)
            elif msg.message.startswith("*余额"):
                self.__deal_with_query_bill(msg)
            elif msg.message.startswith("*欠费"):
                self.__deal_with_arrearage_user(msg)
            elif msg.message.startswith("*积分"):
                self.__deal_with_accumulate_points(msg)

    def __deal_with_call_me(self, msg):
        content = "@%s,您好，请问您有什么指示\\n我现在可以执行以下指令：\\n【*查询】：查询您账户信息\\n【*活动】：查询最近7天的活动\\n【*周X】：查看周X的活动详情\\n【*报名周X】：报名周X的活动，如果外挂请用+y男/女来指定，例如：报名周六+1女+2男\\n【*取消周X】:取消周X的报名\\n" % msg.from_user.card
        content += "【*余额】：查询自己账户余额变更信息\\n"
        content += "【*欠费】：查询所有欠费账户\\n"
        content += "【*积分】：查询自己积分变更信息\\n"
        msg.message = content
        self.chat_module.send_message(msg)

    def __deal_with_arrearage_user(self, msg):
        self.__check_user(msg)
        msg.message = self.qq_account_manager.get_arrearage_user_message()
        logging.info("ARREARAGE_QUERY:%s", msg.message)
        self.chat_module.send_message(msg)

    def __deal_with_query_bill(self, msg):
        self.__check_user(msg)
        msg.message = self.bill_details_manager.get_bill_details_message(msg.from_user)
        logging.info("BILL_QUERY:%s", msg.message)
        self.chat_module.send_message(msg)

    def __deal_with_query_account(self, msg):
        self.__check_user(msg)
        msg.message = QUERY_ACCOUNT_REPLY_PATTEN.format(user=msg.from_user)
        logging.info("ACCOUNT_QUERY:%s", msg.message)
        self.chat_module.send_message(msg)

    def __deal_with_query_activities(self, msg):
        self.__check_user(msg)
        msg.message = self.activity_manager.get_query_activities_message()
        logging.info("ACTIVITIES_QUERY:%s", msg.message)
        self.chat_module.send_message(msg)

    def __deal_with_query_activity(self, msg):
        content = msg.message
        content = content.replace(" ", "")
        content = content.replace("*", "")
        self.__check_user(msg)
        msg.message = self.activity_manager.get_query_activity_message(content)
        logging.info("ACTIVITIES_QUERY:%s", msg.message)
        if msg.message:
            self.chat_module.send_message(msg)


    def __deal_with_enroll(self, msg):
        self.__check_user(msg)
        msg.message = self.enroll_manager.enroll(msg)
        logging.info("ENROLL:%s", msg.message)
        self.chat_module.send_message(msg)

    def __deal_with_cancel_enroll(self, msg):
        self.__check_user(msg)
        msg.message = self.enroll_manager.cancel(msg)
        logging.info("CANCEL ENROLL:%s", msg.message)
        self.chat_module.send_message(msg)

    def __check_user(self, msg):
        user = msg.from_user
        qq_user = self.qq_account_manager.get_user(user)
        if not qq_user:
            qq_user = user
            if not qq_user.card:
                qq_user.card = qq_user.nick_name
            self.qq_account_manager.insert_user(qq_user)

        msg.from_user = qq_user

    def __deal_with_accumulate_points(self, msg):
        self.__check_user(msg)
        msg.message = self.bill_details_manager.get_accumulate_points_details_message(msg.from_user)
        logging.info("ACCUMULATE_QUERY:%s", msg.message)
        self.chat_module.send_message(msg)

    def __reply_group_message(self, msg):
        pass



