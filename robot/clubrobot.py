# -*- coding:utf8 -*-
__author__ = 'changyuf'

import logging
from qqadapter.qqclient import QQClient
from qqadapter.core.qqconstants import QQConstants
from qqadapter.utilities.utilities import WebQQException
from robot.message_processor import MessageProcessor
from qqadapter.module.db_module import DBModule


def begin_poll_message(qq_client, processor):
    while True:
        msg = qq_client.poll_message()
        if msg:
            processor.process(msg)
    return True

if __name__ == '__main__':
    logging.basicConfig(filename=QQConstants.LOG_FILE, level=logging.INFO)
    logging.info("\n\n******************** START ********************")
    # client = QQClient('3173831764', '123456789')  #小秘书

    # client = QQClient('2899530487', '123456789')
    #client = QQClient('3106426008', 'leepet123')
    client = QQClient('3047296752', '123456789')
    db_module = DBModule("104.131.158.219", "changyuf", "changyuf", "club_robot")
    msg_processor = MessageProcessor(client.chat_module, db_module)
    try:
        client.login()
        client.get_friend_info(client.context.account)
        client.get_category_list()
        client.get_group_list()

        for group in client.context.store.group_map.values():
            if group.name == "运动测试" or group.name == "后沙峪友瑞羽毛球群":
                print "开始获取群详细信息.群名：%s" % group.name
                #logging("开始获取群详细信息")
                client.get_group_info(group)
                client.get_group_member_qq(group)
                #logging("获取群详细信息结束.")
    except WebQQException, e:
        logging.exception("Login failed.")
        logging.info("******************** END ********************\n\n")

    print "登录成功，开始接受消息"

    begin_poll_message(client, msg_processor)



