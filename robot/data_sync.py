# -*- coding:utf8 -*-
__author__ = 'changyuf'

import logging


class DataSync:
    def __init__(self, db):
        self.db = db

    def sync_user(self, user):
        user_in_db = self.db.get_user(user)
        if user_in_db:
            self.db.update_db_info(user)
        else: #新用户，直接插入数据库
            self.db.insert_user(user)
            logging.info("A new user added. 昵称：%s, QQ:%s", user.nick_name, user.qq)
            return

    def sync_group(self, group):
        for member in group.members:
            self.sync_user(member)
