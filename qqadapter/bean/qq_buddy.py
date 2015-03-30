# -*- coding:utf8 -*-
__metaclass__ = type
__author__ = 'changyuf'

from qqadapter.bean.qquser import QQUser


class QQBuddy(QQUser):
    def __init__(self):
        super(QQBuddy, self).__init__()
        self.mark_name = ''  # 备注
        self.category = None  # 好友分组 QQCategory

    def __str__(self):
        print "type of nick_name:", type(self.nick_name)
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        #return self.nick_name + "\n"
        out_str = u"Uin:" + self.uin + u"\t昵称：" + self.nick_name
        if self.mark_name:
            out_str += u"\t备注：" + self.mark_name

        return out_str



if __name__ == '__main__':
    buddy = QQBuddy()
    buddy.uin = "123456789"
    buddy.nick_name = "我是昵称".decode("utf-8")
    buddy.mark_name = "我是备注".decode("utf-8")

    print str(buddy)

    aa = "测试"
    bb = "测试"
    print aa == bb

