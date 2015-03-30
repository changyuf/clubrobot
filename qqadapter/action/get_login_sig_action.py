# -*- coding:utf8 -*-
__author__ = 'changyuf'

import requests
import re
import cookielib
from qqadapter.core.qqconstants import QQConstants
from qqadapter.core.qqsession import QQSession
from qqadapter.utilities.utilities import HttpCookies


class GetLoginSigAction:
    @staticmethod
    def get_log_sig(session):
        url = QQConstants.URL_LOGIN_PAGE
        r = requests.get(url, headers=QQConstants.GET_HEADERS)
        HttpCookies.save_cookies(r.cookies)

        # REGXP_LOGIN_SIG
        url = 'var g_login_sig=encodeURIComponent\("(.*?)"\)'
        m = re.search(url, r.content)
        if m:
            session.login_sig = m.group(1)
            return True
        else:
            return False


if __name__ == "__main__":
    session = QQSession()
    r = GetLoginSigAction.get_log_sig(session)
    if r:
        print session.login_sig
    else:
        print "get log sig failed"
