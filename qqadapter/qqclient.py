# -*- coding:utf8 -*-

__author__ = 'changyuf'

import requests
import logging
import time
from qqadapter.core.qqsession import QQSession
from qqadapter.action.get_login_sig_action import GetLoginSigAction
from qqadapter.action.check_verify_action import CheckVerifyAction
from qqadapter.bean.qquser import QQAccount
from qqadapter.utilities.utilities import HttpCookies
from qqadapter.action.web_login_action import WebLoginAction
from qqadapter.action.get_captcha_image_action import GetCaptchaImageAction
from qqadapter.action.check_login_sig_action import CheckLoginSigAction
from qqadapter.action.channel_login_action import ChannelLoginAction
from qqadapter.module.user_module import UserModule
from qqadapter.module.group_module import GroupModule
from qqadapter.module.category_module import CategoryModule
from qqadapter.core.qqstore import QQStore
from qqadapter.action.poll_message_action import PollMessageAction
from qqadapter.core.qqconstants import QQConstants
from qqadapter.module.login_module import LoginModule
from qqadapter.core.qq_context import QQContext
from qqadapter.module.poll_message_module import PollMessageModule
from qqadapter.module.chat_module import ChatModule


class QQClient:
    def __init__(self, user_name, password):
        self.context = QQContext(user_name, password)
        self.group_module = GroupModule(self.context)
        self.category_module = CategoryModule(self.context)
        self.login_module = LoginModule(self.context)
        self.user_module = UserModule(self.context)
        self.poll_message_module = PollMessageModule(self.context, self.user_module)
        self.chat_module = ChatModule(self.context)

    def login(self):
        self.login_module.login()

    def get_category_list(self):
        self.category_module.get_category_list()

    def get_friend_info(self, user):
        return self.user_module.get_friend_info(user)

    def get_stranger_info(self, user):
        return self.user_module.get_stranger_info(user)

    def get_group_info(self, group):
        self.group_module.get_group_info(group)

    def get_group_list(self):
        self.group_module.get_group_list()

    def get_user_account(self, user):
        self.user_module.get_user_account(user)

    def get_group_member_qq(self, group):
        for member in group.members:
            self.user_module.get_user_account(member)

    def poll_message(self):
        if self.context.qq_session.state == QQSession.State.OFFLINE:
            logging.error("client is already offline, can not poll message")
            return None
        ret = self.poll_message_module.poll_message()
        retcode = ret[0]
        if retcode == 0:
            return ret[1]

        if retcode == 102:
            logging.info("没有消息")
            # 接连正常，没有消息到达 {"retcode":102,"errmsg":""}
        elif retcode == 110 or retcode == 109: # 客户端主动退出
            self.context.qq_session.state = QQSession.State.OFFLINE
        elif retcode == 116:
            # 需要更新ptwebqq值，暂时不知道干嘛用的
            # {"retcode":116,"p":"2c0d8375e6c09f2af3ce60c6e081bdf4db271a14d0d85060"}
            # if (a.retcode === 116) alloy.portal.setPtwebqq(a.p)
            self.context.qq_session.ptwebqq = ret[1] # "p"));
        elif retcode == 121 or retcode == 120 or retcode == 100 or retcode == 250:
            # 121,120 : ReLinkFailure	100 : NotReLogin 250 :
            # 服务器需求重新认证
            # {"retcode":121,"t":"0"}
            logging.info("**** NEED_REAUTH retcode: %d %s", retcode, " ****")
            self.context.qq_session.state = QQSession.State.OFFLINE
            self.login_module.channel_login()
        else:
            logging.error("**Reply retcode to author**")
            logging.error("***************************")
            logging.error("Unknown retcode: %d", retcode)
            logging.error("***************************")
            # 遇到未知retcode
            self.context.qq_session.state = QQSession.State.ERROR
            self.login_module.channel_login()

        return None





        #self.store.print_category_info()



if __name__ == "__main__":
    client = QQClient('3173831764', '123456789')  #小秘书
    logging.basicConfig(filename=QQConstants.LOG_FILE, level=logging.INFO)
    client = QQClient('3173831764', '123456789')
    #client = QQClient('2899530487', '123456789')
    #client = QQClient('3106426008', 'leepet123')
    #client = QQClient('3047296752', '123456789')
    # 3047296752
    #3173831764
    client.login()
