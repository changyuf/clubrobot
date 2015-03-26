# -*- coding:utf8 -*-
__author__ = 'changyuf'

import requests
import json
from qqadapter.core.qqconstants import QQConstants
from qqadapter.utilities.utilities import HttpCookies

class ChannelLoginAction:
    def __init__(self):
        pass

    @staticmethod
    def channel_login():
        #URL_CHANNEL_LOGIN =
        url = "http://d.web2.qq.com/channel/login2"

        payload = {'some': 'data'}


        r = requests.post(url, data=json.dumps(payload), headers=QQConstants.HEADERS)
        print r.content
        print r.headers
        HttpCookies.save_cookies(r.cookies)

        if r.status_code == '200':
            return True

        return False
