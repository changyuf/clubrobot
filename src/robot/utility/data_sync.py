# -*- coding:utf8 -*-
__author__ = 'changyuf'

import logging


class DataSync:
    def __init__(self, qq_account_manager):
        self.qq_account_manager = qq_account_manager

    def sync_user(self, user):
        user_in_db = self.qq_account_manager.get_user(user)
        if user_in_db:
            self.qq_account_manager.update_db_info(user)
        else:  # 新用户，直接插入数据库
            self.qq_account_manager.insert_user(user)
            logging.info("A new user added. 昵称：%s, QQ:%s", user.nick_name, user.qq)
            return

    def sync_group(self, group):
        for member in group.members:
            self.sync_user(member)
