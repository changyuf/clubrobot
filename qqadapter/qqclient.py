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


class QQClient:
    def __init__(self, user_name, password):
        self.context = QQContext(user_name, password)
        self.group_module = GroupModule(self.context)
        self.category_module = CategoryModule(self.qq_session, self.request_session, self.account, self.store)
        self.login_module = LoginModule(self.context)
        self.user_module = UserModule(self.context)
        self.poll_message_module = PollMessageModule(self.context)

    def login(self):
        return self.login_module.login()

    def get_friend_info(self, user):
        return self.user_module.get_friend_info(user)

    def get_stranger_info(self, user):
        return self.user_module.get_stranger_info(user)

    def poll_message(self):
        if self.context.qq_session.state == QQSession.State.OFFLINE:
            logging.error("client is already offline, can not poll message")
            return None
        ret = self.poll_message_module.poll_message()
        retcode = ret[0]
        if retcode == 0:
            return ret[1]

        if retcode == 102:
            # 接连正常，没有消息到达 {"retcode":102,"errmsg":""}
            return None

        if retcode == 110 or retcode == 109: # 客户端主动退出
            self.context.qq_session.state = QQSession.State.OFFLINE
        elif retcode == 116:
            # 需要更新ptwebqq值，暂时不知道干嘛用的
            # {"retcode":116,"p":"2c0d8375e6c09f2af3ce60c6e081bdf4db271a14d0d85060"}
            # if (a.retcode === 116) alloy.portal.setPtwebqq(a.p)
            self.context.qq_session.ptwebqq = ret[1] # "p"));
        elif retcode == 121 or retcode == 120 or retcode == 100: # 121,120 : ReLinkFailure	100 : NotReLogin
            # 服务器需求重新认证
            # {"retcode":121,"t":"0"}
            LOG.info("**** NEED_REAUTH retcode: " + retcode + " ****");
            getContext().getSession().setState(QQSession.State.OFFLINE);
            QQException ex = new QQException(QQException.QQErrorCode.INVALID_LOGIN_AUTH);
            notifyActionEvent(QQActionEvent.Type.EVT_ERROR, ex);
            return;
            //notifyEvents.add(new QQNotifyEvent(QQNotifyEvent.Type.NEED_REAUTH, null));
        } else {

            LOG.error("**Reply retcode to author**");
            LOG.error("***************************");
            LOG.error("Unknown retcode: " + retcode);
            LOG.error("***************************");
            // 返回错误，核心遇到未知retcode
            // getContext().getSession().setState(QQSession.State.ERROR);
            notifyEvents.add(new QQNotifyEvent(QQNotifyEvent.Type.UNKNOWN_ERROR, json));
        }

        UserModule.get_friend_info(self.qq_session, self.account, self.request_session)
        self.group_module.get_group_list()
        print ""
        print "开始获取群详细信息"
        for group in self.store.group_map.values():
            print group.name
            self.group_module.get_group_info(group)
        print "获取群详细信息结束"

        self.category_module.get_category_list()
        self.begin_poll_message()



        #self.store.print_category_info()

    def begin_poll_message(self):
        if self.qq_session.state == QQSession.State.OFFLINE:
            print "client is already offline !!!"
            return False
        poll_message_action = PollMessageAction(self.qq_session, self.request_session, self.account, self.store, self.group_module)
        while True:
            poll_message_action.poll_message()
            time.sleep(2)



    def __get_log_sig(self):
        return GetLoginSigAction.get_log_sig(self.qq_session)

    def __check_verify(self):
        ret = CheckVerifyAction.check_verify(self.qq_session, self.account.user_name, self.request_session)
        self.verify_code = ret[1]
        self.account.uin_hex = ret[2]

        # test
        print "uin:"
        print self.account.uin_hex

        if ret[0] == '1':
            return True
        return False


    def __read_verify_code(self, reason):
        GetCaptchaImageAction.get_captcha_image(self.account, self.request_session)
        return raw_input(reason + ":")


if __name__ == "__main__":
<<<<<<< HEAD
    client = QQClient('3173831764', '123456789')  #小秘书
=======
    logging.basicConfig(filename=QQConstants.LOG_FILE, level=logging.INFO)
    client = QQClient('3173831764', '123456789')
>>>>>>> 0deed5a804bd0dd61da71038009468b688a4cfa6
    #client = QQClient('2899530487', '123456789')
    #client = QQClient('3106426008', 'leepet123')
    #client = QQClient('3047296752', '123456789')
    # 3047296752
    #3173831764
    client.login()
