# -*- coding:utf8 -*-
__author__ = 'changyuf'

# deprecated file
import re
import random
from qqadapter.core.qqconstants import QQConstants
from qqadapter.utilities.utilities import HttpCookies


class CheckVerifyAction:
    @staticmethod
    def check_verify(qq_session, user, requests_session):
        url = QQConstants.URL_CHECK_VERIFY.format(user, qq_session.login_sig, random.random())
        r = requests_session.get(url, headers=QQConstants.GET_HEADERS)

        HttpCookies.save_cookies(r.cookies)

        # REGXP_CHECK_VERIFY
        regxp = "ptui_checkVC\('(.*?)','(.*?)','(.*?)'(,\s*'(.*?)')?\)"

        m = re.search(regxp, r.content)
        #print "group0:" + m.group(0)
        #print "group1:" + m.group(1)
        #print "group2:" + m.group(2)
        #print "group3:" + m.group(3)

        result = m.group(1)
        verify_code = m.group(2)
        uin = m.group(3).replace("\\x", "")

        #return result, verify_code, long(uin, 16)
        return result, verify_code, uin


if __name__ == '__main__':
    str = "ptui_checkVC('0','!PAR','\\x00\\x00\\x00\\x00\\xac\\xd3\\x52\\xf7','b1097cfb6dff0d85d925b9ff2ac40f014fc83ceb83746b87791f7211b945f1d520d88c208a374e87e33381054c92c5ca','0')"
    regxp = "ptui_checkVC\('(.*?)','(.*?)','(.*?)'(,\s*'(.*?)')?\)"

    print "str:" + str
    m = re.search(regxp, str)
    print "group0:" + m.group(0)
    print "group1:" + m.group(1)
    print "group2:" + m.group(2)
    print "group3:" + m.group(3)
    uni = m.group(3)
    uni = uni.replace("\\x", "")
    print "uni:" + uni