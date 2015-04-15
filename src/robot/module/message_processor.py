# -*- coding:utf8 -*-
__author__ = 'changyuf'

import logging
from qqadapter.bean.qq_message import QQMessage
from robot.module.activity_manager import ActivityManager
from robot.module.enroll_manager import EnrollManager
from robot.utility.config import Config
from robot.module.bill_details_manager import BillDetailsManager
from robot.module.weather_manager import WeatherManager

QUERY_ACCOUNT_REPLY_PATTEN = """会员名：{user.card}   性别：{user.gender}\\n会员级别：{user.club_level}\\n账户余额：{user.balance}\\n参加活动次数：{user.activity_times}\\n积分：{user.accumulate_points}"""


class MessageProcessor:
    def __init__(self, qq_client, qq_account_manager):
        self.qq_client = qq_client
        self.chat_module = qq_client.chat_module
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
        # if group_name == "运动测试" or group_name == "后沙峪友瑞羽毛球群":
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
            elif msg.message.startswith("*自评"):
                self.__deal_with_update_comments(msg)
            elif msg.message.startswith("*评价"):
                self.__deal_with_update_other_comments(msg)
            elif msg.message.startswith("*天气"):
                self.__deal_with_weather(msg)
            elif msg.message.startswith("*更新"):
                self.__deal_update_user_info(msg)

    def __deal_with_call_me(self, msg):
        content = "@%s,您好，请问您有什么指示\\n我现在可以执行以下指令：\\n【*查询】：查询您账户信息\\n【*活动】：查询最近7天的活动\\n【*周X】：查看周X的活动详情\\n【*报名周X】：报名周X的活动，如果外挂请用+y男/女来指定，例如：报名周六+1女+2男\\n【*取消周X】:取消周X的报名\\n" % msg.from_user.card
        content += "【*余额】：查询自己账户余额变更信息\\n"
        content += "【*欠费】：查询所有欠费账户\\n"
        content += "【*积分】：查询自己积分变更信息\\n"
        content += "【*自评】：修改自我评价\\n"
        content += "【*评价】：评价别人,例如：*评价 test 英明神武\\n"
        content += "【*天气】：查询北京天气\\n"
        content += "【*更新】：修改系统中自己的群名片或者性别\\n"
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
        message = msg.message
        message = message.replace("*查询", "")
        card = message.strip()
        if not card:
            self.__deal_with_query_self_account(msg)
        else:
            self.__deal_with_query_other_account(msg, card)

    def __deal_with_query_self_account(self, msg):
        message = QUERY_ACCOUNT_REPLY_PATTEN.format(user=msg.from_user)
        if msg.from_user.comments:
            message += "\\n自我评价：%s" % msg.from_user.comments
        if msg.from_user.other_comments:
            message += "\\n别人评价：%s" % msg.from_user.other_comments
        msg.message = message
        logging.info("ACCOUNT_QUERY:%s", msg.message)
        self.chat_module.send_message(msg)

    def __deal_with_query_other_account(self, msg, card):
        users = self.qq_account_manager.get_user_by_card(card)
        if not users:
            msg.message = "俱乐部没有会员'%s'" % card
            self.chat_module.send_message(msg)
            return

        for qq_user in users:
            message = QUERY_ACCOUNT_REPLY_PATTEN.format(user=qq_user)
            if qq_user.comments:
                message += "\\n自我评价：%s" % qq_user.comments
            if qq_user.other_comments:
                message += "\\n别人评价：%s" % qq_user.other_comments
            msg.message = message
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
        if not user.qq:
            self.qq_client.get_user_account(user)

        qq_user = self.qq_account_manager.get_user(user)
        if not qq_user:
            qq_user = user
            if not qq_user.card:
                qq_user.card = qq_user.nick_name
            self.qq_account_manager.insert_user(qq_user)
        else:
            qq_user.uin = user.uin

        msg.from_user = qq_user

    def __deal_with_accumulate_points(self, msg):
        self.__check_user(msg)
        msg.message = self.bill_details_manager.get_accumulate_points_details_message(msg.from_user)
        logging.info("ACCUMULATE_QUERY:%s", msg.message)
        self.chat_module.send_message(msg)

    def __deal_with_update_comments(self, msg):
        self.__check_user(msg)
        msg.message = self.qq_account_manager.update_user_comments(msg)
        logging.info("UPDATE_COMMENTS:%s", msg.message)
        self.chat_module.send_message(msg)

    def __deal_with_update_other_comments(self, msg):
        self.__check_user(msg)
        msg.message = self.qq_account_manager.update_user_other_comments(msg)
        logging.info("UPDATE_OTHER_COMMENTS:%s", msg.message)
        self.chat_module.send_message(msg)

    def __deal_update_user_info(self, msg):
        self.__check_user(msg)
        group = msg.group
        self.qq_client.get_group_info(group)
        user = group.get_member_by_uin(msg.from_user.uin)
        ret = self.qq_account_manager.update_db_info(user)
        if ret:
            message = "@%s 更新用户信息成功" % user.card
        else:
            message = "@%s 更新用户信息失败" % user.card
        msg.message = message
        logging.info("UPDATE_USER_INFO:%s", msg.message)
        self.chat_module.send_message(msg)

    def __deal_with_weather(self, msg):
        msg.message = WeatherManager.get_weather_message()
        logging.info("UPDATE_OTHER_COMMENTS:%s", msg.message)
        self.chat_module.send_message(msg)

    def __reply_group_message(self, msg):
        pass



