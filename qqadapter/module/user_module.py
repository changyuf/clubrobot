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
    def get_friend_info(qq_session, user, requests_session):
        #URL_GET_FRIEND_INFO
        url = "http://s.web2.qq.com/api/get_friend_info2"
        parameters = {
            'tuin': str(user.uin),
            'verifysession':"",
            'code': '',
            'vfwebqq':qq_session.vfwebqq,
            't': str(int(time.time()))
        }
        #response = requests.session().get(url, params=parameters, headers=QQConstants.HEADERS)
        response = requests_session.get(url, params=parameters, headers=QQConstants.GET_HEADERS)

        print "response for get_friend_info"
        print response.content

        print "response.json:"
        print response.json()


