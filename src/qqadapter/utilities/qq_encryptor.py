# -*- coding:utf8 -*-
__author__ = 'changyuf'

import platform

if platform.system() == "Windows":
    import win32com.client
else:
    import spidermonkey

from qqadapter.bean.qquser import QQAccount
from robot.utility.config import Config


class QQEncryptor:
    if platform.system() != "Windows":
        rt = spidermonkey.Runtime()
        cx = rt.new_context()

    def __init__(self):
        pass

    @classmethod
    def encrypt2(cls, qq_account, verify_code):
        if platform.system() == "Windows":
            return QQEncryptor.__encrypt_windows(qq_account, verify_code)
        else:
            return QQEncryptor.__encrypt_linux(qq_account, verify_code)

    @classmethod
    def __encrypt_linux(cls, qq_account, verify_code):
        config = Config()
        mq_comm_js = config.get("qq_adapter", "mq_comm_js_linux")
        fs = open(mq_comm_js, "r")
        func = cls.cx.execute(fs.read())
        fs.close()
        return func(qq_account.password, qq_account.uin_hex, verify_code)

    @classmethod
    def __encrypt_windows(cls, qq_account, verify_code):
        js = win32com.client.Dispatch('MSScriptControl.ScriptControl')
        js.Language = 'JavaScript'
        js.AllowUI  = False
        config = Config()
        mq_comm_js = config.get("qq_adapter", "mq_comm_js_windows")
        fs = open(mq_comm_js, "r")
        js.AddCode(fs.read())
        fs.close()
        return js.Run("getPassword", qq_account.password, qq_account.uin_hex, verify_code)

    @classmethod
    def hash(cls, uin, ptwebqq):
        if platform.system() == "Windows":
            return QQEncryptor.__hash_windows(uin, ptwebqq)
        else:
            return QQEncryptor.__hash_linux(uin, ptwebqq)

    @classmethod
    def __hash_windows(cls, uin, ptwebqq):
        js = win32com.client.Dispatch('MSScriptControl.ScriptControl')
        js.Language = 'JavaScript'
        js.AllowUI  = False
        config = Config()
        hash_js = config.get("qq_adapter", "hash_js_windows")
        fs = open(hash_js, "r")
        js.AddCode(fs.read())
        fs.close()
        return js.Run("hash", uin, ptwebqq)

    @classmethod
    def __hash_linux(cls, uin, ptwebqq):
        config = Config()
        hash_js = config.get("qq_adapter", "hash_js_linux")
        fs = open(hash_js, "r")
        func = cls.cx.execute(fs.read())
        fs.close()
        return func(uin, ptwebqq)



if __name__ == '__main__':
    account = QQAccount("3047296752", "123456789")
    account.uin_hex = 'b7a2c9fad2e2cde2'


    print QQEncryptor.encrypt2(account, "UFDS")

    print QQEncryptor.hash(3047296752, "c7d59afb952cb49dc0a68619e9899e0b290078fe23ddfc2d3ad03708ebfa89a2")