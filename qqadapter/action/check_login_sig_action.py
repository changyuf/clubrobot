# -*- coding:utf8 -*-
__author__ = 'changyuf'

import requests
from qqadapter.core.qqconstants import QQConstants
from qqadapter.utilities.utilities import HttpCookies

class CheckLoginSigAction:
    def __init__(self):
        pass

    @staticmethod
    def check_login_sig(url):
        #print "URL in check_login_sig:" + url
        r = requests.get(url, headers=QQConstants.HEADERS)
        #print r.content
        print r.headers
        print r.cookies
        HttpCookies.save_cookies(r.cookies)

        if r.status_code == '200':
            return True

        return False
