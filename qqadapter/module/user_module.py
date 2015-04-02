# -*- coding:utf8 -*-
__author__ = 'changyuf'

import time
import logging
from qqadapter.utilities.utilities import WebQQException

class UserModule(object):
    def __init__(self, context):
        self.context = context

    def get_friend_info(self, user):
        #URL_GET_FRIEND_INFO
        url = "http://s.web2.qq.com/api/get_friend_info2"
        parameters = {
            'tuin': str(user.uin),
            'verifysession':"",
            'code': '',
            'vfwebqq':self.context.qq_session.vfwebqq,
            't': str(int(time.time()))
        }

        response = self.context.http_service.get(url, parameters)
        if not response:
            raise WebQQException("get_friend_info failed")
        logging.info("response of GET_FRIEND_INFO:%s", response.content)

        data =  response.json()
        UserModule.__parse_user_info(data, user)

    def get_stranger_info(self, user):
        # URL_GET_STRANGER_INFO
        url = "http://s.web2.qq.com/api/get_stranger_info2"
        parameters = {
            'tuin': str(user.uin),
            'verifysession':"",
            'gid':0,
            'code': '',
            'vfwebqq':self.context.qq_session.vfwebqq,
            't': str(int(time.time()))
        }

        response = self.context.http_service.get(url, parameters)
        if not response:
            raise WebQQException("get_friend_info failed")
        logging.info("response of GET_STRANGER_INFO:%s", response.content)

        data =  response.json()
        UserModule.__parse_user_info(data, user)

    @staticmethod
    def __parse_user_info(data, user):
        if data["retcode"] != 0:
            logging("get user info failed. retcode:%s", data["retcode"])
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
        #     user.setVipLevel(obj.getInt("vip_info")); # VIP等级 0为非VIP
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
        return True


