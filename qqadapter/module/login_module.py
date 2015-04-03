# -*- coding:utf8 -*-
__author__ = 'changyuf'

import re
import json
import urllib
import shutil
import random
import logging
from qqadapter.core.qqconstants import QQConstants
from qqadapter.utilities.utilities import WebQQException
from qqadapter.utilities.qq_encryptor import QQEncryptor
from qqadapter.core.qqsession import QQSession


class LoginModule:
    def __init__(self, context):
        self.context = context
        self.need_verify = False
        self.login_sig = None
        self.verify_code = None

    def login(self):
        self.__get_log_sig()
        self.__check_verify()

        if self.need_verify:
            self.verify_code = self.__read_verify_code('为了保证您账号的安全，请输入验证码中字符继续登录')

        web_login_ret = self.__web_login()
        while web_login_ret[0] == '4':
            self.verify_code = self.__read_verify_code(web_login_ret[2])
            web_login_ret = self.__web_login()

        if web_login_ret[0] != '0':
            raise WebQQException("Login failed. retcode:%d", web_login_ret[0] )

        self.__check_login_sig(web_login_ret[1])

        self.channel_login()
        return True


    def __get_log_sig(self):
        url = QQConstants.URL_LOGIN_PAGE
        response = self.context.http_service.get(url)
        if not response:
            raise WebQQException("__get_log_sig failed")
        #logging.info("response of GET_LOG_SIG:%s", response.content)

        # REGXP_LOGIN_SIG
        rexp = 'var g_login_sig=encodeURIComponent\("(.*?)"\)'
        m = re.search(rexp, response.content)
        if not m:
            raise WebQQException("__get_log_sig failed, rexp=%s" % rexp)

        self.login_sig = m.group(1)
        return True


    def __check_verify(self):
        user_name = self.context.account.user_name
        url = QQConstants.URL_CHECK_VERIFY.format(user_name, self.login_sig, random.random())
        response = self.context.http_service.get(url)
        if not response:
            raise WebQQException("__check_verify failed")
        logging.info("response of CHECK_VERIFY:%s", response.content)

        # REGXP_CHECK_VERIFY
        regxp = "ptui_checkVC\('(.*?)','(.*?)','(.*?)'(,\s*'(.*?)')?\)"
        m = re.search(regxp, response.content)

        self.verify_code = m.group(2)
        self.context.account.uin_hex = m.group(3).replace("\\x", "")
        self.need_verify = m.group(1) == '1'

    def __web_login(self):
        # URL_UI_LOGIN
        url = "https://ssl.ptlogin2.qq.com/login"
        parameters = self.__construct_web_login_parameters()
        response = self.context.http_service.get(url, parameters)
        if not response:
            raise WebQQException("__web_login failed")
        logging.info("response of WEB_LOGIN:%s", response.content)

        # REGXP_LOGIN
        regxp = "ptuiCB\('(\d+)','(\d+)','(.*?)','(\d+)','(.*?)', '(.*?)'\)"

        m = re.search(regxp, response.content)
        result = m.group(1)
        url = m.group(3)
        reason = m.group(5)

        return result, url, reason

    def __construct_web_login_parameters(self):
        if self.need_verify:
            ptvfsession = self.context.http_service.get_cookie_value('verifysession')
            logging.info("verifysession: %s", ptvfsession)
        else:
            ptvfsession = self.context.http_service.get_cookie_value('ptvfsession')
            logging.info("ptvfsession: %s", ptvfsession)

        parameters = {
            'u': self.context.account.user_name,
            'p': QQEncryptor.encrypt2(self.context.account, self.verify_code),
            'verifycode': self.verify_code,
            'webqq_type': '10',
            'remember_uin': '1',
            'login2qq': '1',
            'aid': '1003903',
            'u1': 'http://web.qq.com/loginproxy.html?login2qq=1&webqq_type=10',
            'h': '1',
            'ptredirect': '0',
            'ptlang': '2052',
            'daid': '164',
            'from_ui': '1',
            'pttype': '1',
            'dumy': '',
            'fp': 'loginerroralert',
            'action': '2-12-26161',
            'mibao_css': 'm_webqq',
            't': '1',
            'g': '1',
            'js_type': '0',
            'js_ver': QQConstants.JSVER,
            'login_sig': self.login_sig,

            # 2015-03-02 登录协议增加的参数
            'pt_uistyle': '5',
            'pt_randsalt': '0',
            'pt_vcode_v1': '0',
            'pt_verifysession_v1': ptvfsession
        }

        return parameters

    def __read_verify_code(self, reason):
        self.__get_captcha_image()
        return raw_input(reason + ":")

    def __get_captcha_image(self):
        # URL_GET_CAPTCHA
        url = "http://captcha.qq.com/getimage";
        parameters = {
            'aid': QQConstants.APPID,
            'r': str(random.random()),
            'uin': str(self.context.account.uin)
        }

        response = self.context.http_service.get(url, parameters)
        if not response:
            raise WebQQException("__get_captcha_image failed")

        with open("verify_2.png", 'wb') as outfile:
            outfile.write(response.content)

        with open("verify.png", 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)

    def __check_login_sig(self, url):
        response = self.context.http_service.get(url)
        if not response:
            raise WebQQException("__check_login_sig failed")
        logging.info("response of CHECK_LOGIN_SIG:%s", response.content)

    def channel_login(self):
        # URL_CHANNEL_LOGIN
        url = "http://d.web2.qq.com/channel/login2"
        if not self.context.qq_session.client_id:
            self.context.qq_session.client_id = str(random.randint(1, 99999999))

        payload = json.dumps({
            "status": "online",
            "ptwebqq": self.context.http_service.get_cookie_value('ptwebqq'),
            "clientid": self.context.qq_session.client_id,
            "psessionid": self.context.qq_session.session_id
        })
        post_data = "r=%s" % urllib.quote(payload)
        response = self.context.http_service.post(url, post_data)
        if not response:
            raise WebQQException("__channel_login failed")
        logging.info("response of CHANNEL_LOGIN:%s", response.content)

        try:
            data = json.loads(response.text, encoding='utf-8')
            if data["retcode"] != 0:
                info = "channel login failed! errcode=%s, errmsg=%s" % (data["retcode"], data["errmsg"])
                logging.error(info)
                raise WebQQException(info)

            ret = data["result"]
            self.context.account.uin = str(ret["uin"])
            self.context.account.fake_qq = str(ret["uin"])
            self.context.account.status = ret["status"]
            self.context.qq_session.session_id = ret["psessionid"]
            self.context.qq_session.vfwebqq = ret["vfwebqq"]
            self.context.qq_session.state = QQSession.State.ONLINE
            self.context.qq_session.index = ret["index"]
            self.context.qq_session.port = ret["port"]
        except ValueError:
            logging.exception()
            raise WebQQException("channel login failed json format error")

