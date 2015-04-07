# -*- coding:utf-8 -*-
__author__ = 'changyuf'

from qqadapter.bean.qq_buddy import QQBuddy

class QQCategory:
    def __init__(self):
        self.index = None
        self.sort = None
        self.name = None
        self.buddy_list = []  # QQBuddy list

    def __str__(self):
        return unicode(self).encode('utf-8')

    # def __str__(self):
    #     print "in __str__"
    #     #return unicode(self).encode('utf-8')
    #     return u"分组名:" + self.name + u"\n"

    def __repr__(self):
        return unicode(self).encode('utf-8')
    # def __repr__(self):
    #     return u"分组名:" + self.name + u"\n"

    def display(self):
        print u"分组名:" + self.name + u"\n"
    def __unicode__(self):
        print "in __unicode__"
        return u"分组名:" + self.name + u"\n"
    # # def __str__(self):
    # #     print "in __str__"
    # #     return self.name
    #     # list = ["", self.name, "\n"]
    #     # return "\t".join(list)
    #
    #     #out_str = "gg:".decode("utf-8") + self.name + u"\n".decode("utf-8")
    #     #out_str = "分组名:".decode("'utf-8") + self.name + "\n".decode("'utf-8")
    #     out_str = u"分组名:" + self.name + u"\n"
    #     # for buddy in self.buddy_list:
    #     #      out_str += u"\t" + buddy + u"\n"
    #
    #     return out_str


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
