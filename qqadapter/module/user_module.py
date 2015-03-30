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
        data =  response.json()
        UserModule.__parse_user_info(data, user)

    @staticmethod
    def get_stranger_info(qq_session, user, requests_session):
        # URL_GET_STRANGER_INFO
        url = "http://s.web2.qq.com/api/get_stranger_info2"
        parameters = {
            'tuin': str(user.uin),
            'verifysession':"",
            'gid':0,
            'code': '',
            'vfwebqq':qq_session.vfwebqq,
            't': str(int(time.time()))
        }
        response = requests_session.get(url, params=parameters, headers=QQConstants.GET_HEADERS)

        print "response for get_stranger_info"
        print response.content

        print "response.json:"
        print response.json()
        data =  response.json()
        UserModule.__parse_user_info(data, user)

    @staticmethod
    def __parse_user_info(data, user):
        if data["retcode"] != 0:
            print "get user info failed. retcode:", data["retcode"]
            return False

        result = data["result"]
        # user.setOccupation(obj.getString("occupation"));
        # user.setPhone(obj.getString("phone"));
        # user.setAllow(QQAllow.values()[obj.getInt("allow")]);
        # user.setCollege(obj.getString("college"));
        # if (obj.has("reg_time")) {
        #     user.setRegTime(obj.getInt("reg_time"));
        # }
        user.uin = str(result["uin"])
        # user.setConstel(obj.getInt("constel"));
        # user.setBlood(obj.getInt("blood"));
        # user.setHomepage(obj.getString("homepage"));
        # user.setStat(obj.getInt("stat"));
        # if(obj.has("vip_info")) {
        #     user.setVipLevel(obj.getInt("vip_info")); // VIP等级 0为非VIP
        # }
        # user.setCountry(obj.getString("country"));
        # user.setCity(obj.getString("city"));
        # user.setPersonal(obj.getString("personal"));
        user.nick_name = result["nick"]
        # user.setChineseZodiac(obj.getInt("shengxiao"));
        # user.setEmail("email");
        # user.setProvince(obj.getString("province"));
        # user.setGender(obj.getString("gender"));
        # user.setMobile(obj.getString("mobile"));
        # if (obj.has("client_type")) {
        #     user.setClientType(QQClientType.valueOfRaw(obj.getInt("client_type")));
        # }


