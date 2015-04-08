# -*- coding:utf8 -*-
__author__ = 'changyuf'

import logging
from qqadapter.bean.qq_message import QQMessage
from robot.module.activity_manager import ActivityManager

QUERY_ACCOUNT_REPLY_PATTEN = """会员名：{user.card}   性别：{user.gender}\\n会员级别：{user.club_level}\\n账户余额：{user.balance}\\n参加活动次数：{user.activity_times}\\n积分：{user.accumulate_points}\\n自我评价：{user.comments}\\n别人评价：{user.other_comments}"""
QUERY_ACTIVITY_REPLY_PATTEN = """会员名：{user.card}   性别：{user.gender}\\n会员级别：{user.club_level}\\n账户余额：{user.balance}\\n参加活动次数：{user.activity_times}\\n积分：{user.accumulate_points}\\n自我评价：{user.comments}\\n别人评价：{user.other_comments}"""



class MessageProcessor:
    def __init__(self, chat_module, db):
        self.chat_module = chat_module
        self.db = db
        self.activity_manager = ActivityManager()

    def process(self, msg):
        if msg.type == QQMessage.Type.GROUP_MSG:
            self.__process_group_message(msg)

    def __process_group_message(self, msg):
        group_name = msg.group.name
        if group_name == "运动测试" or group_name == "后沙峪友瑞羽毛球群":
            if msg.message.startswith("#小秘书"):
                self.__deal_with_call_me(msg)
            elif msg.message.startswith("#摸摸"):
                self.__deal_with_query_account(msg)
            elif  msg.message.startswith("#活动"):
                self.__deal_with_query_activity(msg)
            elif  msg.message.startswith("#报名"):
                self.__deal_with_enroll(msg)

    def __deal_with_call_me(self, msg):
        # new_msg = QQMessage()
        # new_msg.message = "叫我干什么，我现在还没长大，什么都干不了"
        # new_msg.group = msg.group
        # new_msg.type = QQMessage.Type.GROUP_MSG
        msg.message = "叫我干什么，我现在还没长大，什么都干不了"
        self.chat_module.send_message(msg)

    def __deal_with_query_account(self, msg):
        self.__check_user(msg)
        msg.message = QUERY_ACCOUNT_REPLY_PATTEN.format(user=msg.from_user)
        logging.info("ACCOUNT_QUERY:%s", msg.message)
        self.chat_module.send_message(msg)

    def __deal_with_query_activity(self, msg):
        self.__check_user(msg)
        msg.message = self.activity_manager.get_query_activity_message(msg.from_user)
        logging.info("ACTIVITY_QUERY:%s", msg.message)
        self.chat_module.send_message(msg)

    def __deal_with_enroll(self, msg):
        self.__check_user(msg)
        msg.message = self.activity_manager.enroll(msg.from_user)
        logging.info("ENROLL:%s", msg.message)
        self.chat_module.send_message(msg)

    def __check_user(self, msg):
        user = msg.from_user
        qq_user = self.db.get_user(user)
        if not qq_user:
            qq_user = user
            self.db.insert_user(qq_user)
        if not qq_user.card:
            qq_user.card = qq_user.nick_name
        msg.from_user = qq_user

    def __reply_group_message(self, msg):
        pass



