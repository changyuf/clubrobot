# -*- coding:utf8 -*-
__author__ = 'changyuf'

import requests
from qqadapter.core.qqconstants import QQConstants
from qqadapter.utilities.utilities import HttpCookies

class CheckLoginSigAction:
    def __init__(self):
        pass

    @staticmethod
    def check_login_sig(url, requests_session):
        print ""
        print "start check_login_sig"
        #print "URL in check_login_sig:" + url
        #r = requests.get(url, headers=QQConstants.HEADERS)
        r = requests_session.get(url, headers=QQConstants.GET_HEADERS)
        #print r.content
        print r.headers
        print r.cookies
        HttpCookies.save_cookies(r.cookies)

        print "r.status_code in check_login_sig:" + str(r.status_code)
        if r.status_code == 200:
            return (True, r.cookies)

        return (False, None)
