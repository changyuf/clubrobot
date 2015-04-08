# -*- coding:utf8 -*-
__author__ = 'changyuf'

import time
import logging

from robot.utility.config import Config
from qqadapter.qqclient import QQClient
from qqadapter.utilities.utilities import WebQQException
from robot.module.message_processor import MessageProcessor
from robot.utility.data_sync import DataSync
from robot.module.qq_account_manager import QQAccountManager


def begin_poll_message(qq_client, processor):
    while True:
        try:
            msg = qq_client.poll_message()
            if msg:
                processor.process(msg)
        except WebQQException, e:
            logging.exception("poll message failed.ignore it, try again.")
        time.sleep(1)
    return True

if __name__ == '__main__':
    config = Config()
    log_file = config.get("robot", "log_file")
    logging.basicConfig(filename=log_file, level=logging.INFO)
    logging.info("\n\n******************** START ********************")
    # client = QQClient('3173831764', '123456789')  #小秘书

    client = QQClient('2899530487', '123456789')
    #client = QQClient('3106426008', 'leepet123')
    #client = QQClient('3047296752', '123456789')
    qq_account_manager = QQAccountManager()
    msg_processor = MessageProcessor(client.chat_module, qq_account_manager)
    data_sync = DataSync(qq_account_manager)
    try:
        client.login()
        client.get_friend_info(client.context.account)
        client.get_category_list()
        client.get_group_list()

        for group in client.context.store.group_map.values():
            if group.name == "运动测试" or group.name == "后沙峪友瑞羽毛球群":
                #logging("开始获取群详细信息")
                client.get_group_info(group)
                client.get_group_member_account(group)
                data_sync.sync_group(group)
                #logging("获取群详细信息结束.")
    except WebQQException, e:
        logging.exception("Login failed.")
        logging.info("******************** END ********************\n\n")
        exit()

    print "登录成功，开始接受消息"

    begin_poll_message(client, msg_processor)



