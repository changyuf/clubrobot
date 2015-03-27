# -*- coding:utf8 -*-
__author__ = 'changyuf'

import requests
import json
import random
import urllib
from qqadapter.core.qqconstants import QQConstants
from qqadapter.utilities.utilities import HttpCookies, WebQQException
from qqadapter.core.qqsession import QQSession


class ChannelLoginAction:
    def __init__(self):
        pass

    @staticmethod
    def channel_login(qq_session, requests_session, account):
        print "start channel_login"
        # URL_CHANNEL_LOGIN
        url = "http://d.web2.qq.com/channel/login2"
        if not qq_session.client_id:
            qq_session.client_id = str(random.randint(1, 99999999))

        print "ptwebqq in cookies:" + HttpCookies.get_value('ptwebqq')

        rdict = json.dumps({
            "status": "online",
            "ptwebqq": HttpCookies.get_value('ptwebqq'),
            "passwd_sig": "",
            "clientid": qq_session.client_id,
            "psessionid": qq_session.session_id}
        )

        post_data = "r=%s&clientid=%s&psessionid=%s" % (urllib.quote(rdict), qq_session.client_id, qq_session.session_id)
        #post_data = "r=%s&clientid=%s&psessionid=%s" % (urllib.quote(rdict), qq_session.client_id, qq_session.session_id)

        print "post_data in channel_login_action:" + post_data
        try:
            #requests_session.headers['Referer'] = QQConstants.REFFER
            response = requests_session.post(url, data=post_data, headers=QQConstants.HEADERS)

            print response.content

            data = json.loads(response.text, encoding='utf-8')
            if data["retcode"] != 0:
                raise WebQQException(
                    "channel login failed! errcode=%s, errmsg=%s" %
                    (data["retcode"], data["errmsg"] )
                )

            ret = data["result"]
            account.uin = ret["uin"]
            account.fake_qq = ret["uin"]
            account.status = ret["status"]
            qq_session.session_id = ret["psessionid"]
            qq_session.vfwebqq = ret["vfwebqq"]
            qq_session.state = QQSession.State.ONLINE
            qq_session.index = ret["index"]
            qq_session.port = ret["port"]
        except ValueError:
            raise WebQQException("channel login failed json format error")

        # payload = {'some': 'data'}
        #
        # r = requests.post(url, data=json.dumps(payload), headers=QQConstants.HEADERS)
        # print r.content
        # print r.headers
        HttpCookies.save_cookies(response.cookies)

        if response.status_code == 200:
            return True
        return False
