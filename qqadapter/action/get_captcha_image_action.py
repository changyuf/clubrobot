# -*- coding:utf8 -*-
__author__ = 'changyuf'

import requests
import re
import random
import shutil
from qqadapter.core.qqconstants import QQConstants
from qqadapter.utilities.utilities import HttpCookies
from qqadapter.bean.qquser import QQAccount
from StringIO import StringIO


class GetCaptchaImageAction:
    def __init__(self):
        pass

    @staticmethod
    def get_captcha_image(qq_account, requests_session):
        #URL_GET_CAPTCHA
        url  = "http://captcha.qq.com/getimage";
        parameters = {
            'aid': QQConstants.APPID,
            'r': str(random.random()),
            'uin': str(qq_account.uin)
        }
        #r = requests.get(url, headers=QQConstants.HEADERS, params=parameters)
        r = requests_session.get(url, headers=QQConstants.GET_HEADERS, params=parameters)
        HttpCookies.save_cookies(r.cookies)
        print r
        #print r.content
        #print r.raw
        #print r.text

        if r.status_code == 200:
            with open("verify_2.png", 'wb') as outfile:
                outfile.write(r.content)

            with open("verify.png", 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            return True

        return False

if __name__ == '__main__':
    qq_account = QQAccount("2899530487", "123456789")
    qq_account.uin_hex = 2899530487
    r = GetCaptchaImageAction.get_captcha_image(qq_account)
    if r:
        print "get image success"
    else:
        print "get image failed"
