# -*- coding:utf8 -*-

__author__ = 'changyuf'

from qqadapter.bean.qq_category import QQCategory
from qqadapter.bean.qq_buddy import QQBuddy

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

