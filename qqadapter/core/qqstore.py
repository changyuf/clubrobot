# -*- coding:utf8 -*-

__author__ = 'changyuf'

from qqadapter.bean.qq_category import QQCategory
from qqadapter.bean.qq_buddy import QQBuddy
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

class QQStore:
    def __init__(self):
        self.buddy_map = {}  # uin => QQBudy, 快速通过uin查找QQ好友
        self.stranger_map = {}  # uin => QQStranger, 快速通过uin查找临时会话用户
        self.category_map = {}  # index => QQCategory
        self.group_map = {}  # code => QQGroup, 快速通过群ID查找群
        self.discuz_map = {}  # did = > QQDiscuz
        self.picture_item_list = {}  # filename -> PicItem 上传图片列表

    def get_group_by_gin(self, gin):
        groups = self.group_map.values()
        for g in groups:
            if g.gin == gin:
                return g
        return None

    def add_group(self, group):
        self.group_map[group.code] = group

    def print_category_info(self):
        print "******** 好友列表  ********"
        for category in self.category_map.values():
            print category.name
            u"分组名:" + category.name + u"\n"
            # des =  "%r" % category
            #category.display()

if __name__ == '__main__':
    buddy = QQBuddy()
    buddy.uin = "123456789"
    buddy.nick_name = "我是昵称"
    buddy.mark_name = "我是备注"

    buddy2 = QQBuddy()
    buddy2.uin = "2"
    buddy2.nick_name = "我是昵称2"
    buddy2.mark_name = "我是备注2"

    category = QQCategory()
    category.name = u"我是分组名"
    category.buddy_list.append(buddy)
    category.buddy_list.append(buddy2)

    category.display()

