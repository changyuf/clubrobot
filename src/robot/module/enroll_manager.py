# -*- coding:utf8 -*-
__author__ = 'changyuf'

import datetime
import logging
from robot.utility.exceptions import WrongMessageException
from robot.bean.participant import Participant
from robot.utility.constants import Constants
from robot.module.participant_manager import ParticipantManager
from robot.module.activity_manager import ActivityManager
from qqadapter.module.db_module import DBModule
from qqadapter.bean.qq_group_member import QQGroupMember
from qqadapter.bean.qq_message import QQMessage


class EnrollManager:
    def __init__(self, activity_manager):
        self.activity_manager = activity_manager
        self.participant_manager = ParticipantManager()

    def cancel(self, msg):
        content = msg.message
        try:
            weekday = EnrollManager.__parse_cancel_message(content)
        except WrongMessageException:
            logging.exception("ENROLL failed.")
            return "@%s,取消报名没成功，输入格式不正确" % msg.from_user.card
        activity = self.__get_activity(weekday)
        if not activity:
            return "@%s,取消报名没成功，输入的日期不对" % msg.from_user.card

        ret = self.participant_manager.get_participant(activity.id, msg.from_user.qq)
        if not ret:
            return "@%s,你还没有报名本次活动" % msg.from_user.card

        ret = self.participant_manager.delete_participant(activity.id, msg.from_user.qq)
        if not ret:
            return "@%s,小秘书心情不好，你本次取消报名没成功，请重试" % msg.from_user.card

        content = "%s  取消报名成功!\\n" % msg.from_user.card
        content += "活动：%s\\n" % activity.title
        content += "地点：【%s】\\n" % activity.activity_position
        content += self.participant_manager.get_participant_message(activity.id, activity.max_participants)

        return content

    def enroll(self, msg):
        content = msg.message
        try:
            ret = EnrollManager.__parse_enroll_message(content)
        except WrongMessageException:
            logging.exception("ENROLL failed.")
            return "@%s,报名没成功，输入格式不正确" % msg.from_user.card

        activity = self.__get_activity(ret[0])
        if not activity:
            return "@%s,报名没成功，%s没有活动" % (msg.from_user.card, Constants.WEEKDAY[ret[0]])

        # 检查是否已经报名
        p = self.participant_manager.get_participant(activity.id, msg.from_user.qq)
        if p:
            return "@%s,你已经报名本次活动，如果需要修改外挂，请先取消报名，再重新报名" % msg.from_user.card

        dt = datetime.datetime.now()
        if dt > activity.dead_line:
            return "@%s,报名没成功，本次活动报名已经截至" % msg.from_user.card

        if msg.from_user.gender == "女":
            needed_money = activity.price_female
        else:
            needed_money = activity.price_male
        needed_money += activity.price_female * ret[1]["女"] + activity.price_male * ret[1]["男"]
        if needed_money > msg.from_user.balance:
            return "@%s,你的余额不足,请充值后再报名." % msg.from_user.card

        participants = self.participant_manager.get_participants(activity.id)
        number = EnrollManager.__get_participants_number(participants)
        if number == activity.max_participants:
            return "@%s,报名没成功，本次活动已经满员" % msg.from_user.card
        needed_position = ret[1]["男"] + ret[1]["女"] + 1
        if number + needed_position > activity.max_participants:
            return "@%s,本次活动的坑已经已经不够你报名%d人" % (msg.from_user.card, needed_position)

        participant = EnrollManager.__construct_participant(msg.from_user, activity.id, ret[1], needed_money)
        ret = self.participant_manager.insert_participant(participant)
        if not ret:
            return "@%s,小秘书心情不好，你本次报名没成功，请重试" % msg.from_user.card

        content = "%s  报名成功!\\n" % msg.from_user.card
        content += "活动：%s\\n" % activity.title
        content += "地点：【%s】\\n" % activity.activity_position
        content += self.participant_manager.get_participant_message(activity.id, activity.max_participants)

        return content


    @staticmethod
    def __construct_participant(user, activity_id, add_on_dict, cost):
        participant = Participant()
        participant.activity_id = activity_id
        if user.card:
            participant.card = user.card
        else:
            participant.card = user.nick_name
        participant.qq = user.qq
        participant.type = "QQ"
        participant.gender = user.gender
        participant.add_on_female = add_on_dict["女"]
        participant.add_on_male = add_on_dict["男"]
        participant.cost = cost

        return participant

    @staticmethod
    def __get_participants_number(participants):
        number = 0
        for participant in participants:
            number += 1 + participant.add_on_male + participant.add_on_female

        return number

    def __get_activity(self, weekday):
        activities = self.activity_manager.get_recent_activities()
        for activity in activities:
            if weekday == activity.start_time.weekday():
                return activity

        return None

    @staticmethod
    def __parse_cancel_message(content):
        content = content.replace(" ", "")
        content = content.replace("#取消报名", "")
        if not content:
            raise WrongMessageException()

        if content not in Constants.WEEKDAY_TO_INDEX.keys():
            raise WrongMessageException()

        weekday = Constants.WEEKDAY_TO_INDEX[content]
        return weekday

    @staticmethod
    def __parse_enroll_message(content):
        content = content.replace(" ", "")
        content = content.replace("#报名", "")
        if not content:
            raise WrongMessageException()
        its = content.split("+")
        num = len(its)
        activity_weekday = its[0]
        if activity_weekday not in Constants.WEEKDAY_TO_INDEX.keys():
            raise WrongMessageException()
        weekday = Constants.WEEKDAY_TO_INDEX[activity_weekday]
        add_on_dict = {"男": 0, "女": 0}
        if num > 1:
            ret = EnrollManager.__parse_add_on(its[1])
            add_on_dict[ret[0]] = ret[1]
        if num > 2:
            ret = EnrollManager.__parse_add_on(its[2])
            add_on_dict[ret[0]] = ret[1]

        return weekday, add_on_dict

    @staticmethod
    def __parse_add_on(text):
        if text[:2].isalnum():
            number = int(text[:2])
            gender = text[2:]
        elif text[:1].isalnum():
            number = int(text[:1])
            gender = text[1:]
        else:
            raise WrongMessageException()
        if gender != "男" and gender != "女":
            raise WrongMessageException()

        return gender, number

if __name__ == "__main__":
    activity_manager = ActivityManager()
    #participant_manager = ParticipantManager()
    user = QQGroupMember()
    user.qq = "17014162"
    db_module = DBModule()
    msg = QQMessage()
    msg.from_user =db_module.get_user(user)
    msg.message = "#报名周六"
    enroll_manager = EnrollManager(activity_manager)
    # print enroll_manager.enroll(msg)
    # print enroll_manager.enroll(msg)
    # msg.message = "#取消报名周六"
    # print enroll_manager.cancel(msg)
    # print enroll_manager.cancel(msg)

    msg.message = "#报名周六+1男+ 2女"
    print enroll_manager.enroll(msg)
    msg.message = "#取消报名周五"
    print enroll_manager.cancel(msg)


