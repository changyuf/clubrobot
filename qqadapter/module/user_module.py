# -*- coding:utf8 -*-
__author__ = 'changyuf'

import time
import requests
from qqadapter.core.qqconstants import QQConstants
from qqadapter.utilities.utilities import HttpCookies, WebQQException

class UserModule(object):
    def __init__(self):
        pass

    @staticmethod
    def get_friend_info(qq_session, user):
        #URL_GET_FRIEND_INFO
        url = "http://s.web2.qq.com/api/get_friend_info2"
        parameters = {
            'tuin': user.uin,
            'verifysession':"",
            'code': '',
            'vfwebqq':qq_session.vfwebqq,
            't': str(int(time.time()))
        }
        response = requests.session().get(url, params=parameters, headers=QQConstants.HEADERS)

        print response.json()


