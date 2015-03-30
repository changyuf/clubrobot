# -*- coding:utf8 -*-
__author__ = 'changyuf'

import platform

if platform.system() == "Windows":
    import win32com.client
else:
    import spidermonkey

from qqadapter.bean.qquser import QQAccount


class QQEncryptor:
    mq_comm_js = "/home/changyuf/workspace/clubrobot/resources/mq_comm_linux.js"
    hash_js = "/home/changyuf/workspace/clubrobot/resources/hash_linux.js"

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
        return func(qq_account.password, qq_account.uin_hex, verify_code)

    @staticmethod
    def __encrypt_windows(qq_account, verify_code):
        js = win32com.client.Dispatch('MSScriptControl.ScriptControl')
        js.Language = 'JavaScript'
        js.AllowUI  = False
        fs = open("qq_comm_windows.js", "r")
        js.AddCode(fs.read())
        return js.Run("getPassword", qq_account.password, qq_account.uin_hex, verify_code)

    @staticmethod
    def hash(uin, ptwebqq):
        if platform.system() == "Windows":
            return QQEncryptor.__hash_windows(uin, ptwebqq)
        else:
            return QQEncryptor.__hash_linux(uin, ptwebqq)

    @staticmethod
    def __hash_windows(uin, ptwebqq):
        js = win32com.client.Dispatch('MSScriptControl.ScriptControl')
        js.Language = 'JavaScript'
        js.AllowUI  = False
        fs = open("hash_windows.js", "r")
        js.AddCode(fs.read())
        return js.Run("hash", uin, ptwebqq)

    @staticmethod
    def __hash_linux(uin, ptwebqq):
        rt = spidermonkey.Runtime()
        cx = rt.new_context()
        fs = open(QQEncryptor.hash_js, "r")
        func = cx.execute(fs.read())
        return func(uin, ptwebqq)



if __name__ == '__main__':
    account = QQAccount("3047296752", "123456789")
    account.uin_hex = 'b7a2c9fad2e2cde2'


    print QQEncryptor.encrypt2(account, "UFDS")

    print QQEncryptor.hash(3047296752, "c7d59afb952cb49dc0a68619e9899e0b290078fe23ddfc2d3ad03708ebfa89a2")