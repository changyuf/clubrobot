__author__ = 'changyuf'

import platform

if platform.system() == "Windows":
    import win32com.client
else:
    import spidermonkey

from qqadapter.bean.qquser import QQAccount


class QQEncryptor:
    mq_comm_js = "/home/changyuf/workspace/clubrobot/resources/mq_comm.js"

    def __init__(self):
        pass

    @staticmethod
    def encrypt2(qq_account, verify_code):
        if platform.system() == "Windows":
            return QQEncryptor.__encrypt_windows(qq_account, verify_code)
        else:
            return QQEncryptor.__encrypt_linux(qq_account, verify_code)

    @staticmethod
    def __encrypt_linux(qq_account, verify_code):
        rt = spidermonkey.Runtime()
        cx = rt.new_context()
        fs = open(QQEncryptor.mq_comm_js, "r")
        func = cx.execute(fs.read())

        #test
        print "uin in qq_account:"
        print qq_account.uin
        print "user_name in qq_account:%s" % qq_account.user_name

        return func(qq_account.password, qq_account.uin, verify_code)

    @staticmethod
    def __encrypt_windows(qq_account, verify_code):
        js = win32com.client.Dispatch('MSScriptControl.ScriptControl')
        #js = win32com.client.Dispatch('MSScriptControl.ScriptControl')
        js.Language = 'JavaScript'
        js.AllowUI  = False
        fs = open("qq_comm.js", "r")
        js.AddCode(fs.read())
        return js.Run("getPassword", qq_account.password, qq_account.user_name, verify_code)


if __name__ == '__main__':
    account = QQAccount("3047296752", "123456789")


    print QQEncryptor.encrypt2(account, "UFDS")