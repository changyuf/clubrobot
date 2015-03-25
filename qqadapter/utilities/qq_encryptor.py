__author__ = 'changyuf'

import spidermonkey
from qqadapter.bean.qquser import QQAccount


class QQEncryptor:
    mq_comm_js = "/home/changyuf/workspace/clubrobot/resources/mq_comm.js"

    def __init__(self):
        pass

    @staticmethod
    def encrypt2(qq_account, verify_code):
        rt = spidermonkey.Runtime()
        cx = rt.new_context()
        fs = open(QQEncryptor.mq_comm_js, "r")
        func = cx.execute(fs.read())

        #test
        print "uin in qq_account:"
        print qq_account.uin
        print "user_name in qq_account:%s" % qq_account.user_name

        return func(qq_account.password, qq_account.uin, verify_code)


if __name__ == '__main__':
    account = QQAccount("3047296752", "123456789")

    print QQEncryptor.encrypt2(account, "UFDS")