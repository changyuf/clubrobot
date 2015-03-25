# -*- coding:utf8 -*-

__author__ = 'changyuf'

import requests
from qqadapter.core.qqconstants import QQConstants
from qqadapter.core.qqsession import QQSession
from qqadapter.utilities.utilities import HttpCookies
from qqadapter.utilities.qq_encryptor import QQEncryptor

class WebLoginAction:
    def __init__(self):
        pass

    @staticmethod
    def login(qq_session, qq_account, verify_code, need_input_verify_code = False):
        #URL_UI_LOGIN
        url = "https://ssl.ptlogin2.qq.com/login"
        parameters = WebLoginAction.__construct_parameters(qq_session, qq_account, verify_code, need_input_verify_code)

        r = requests.get(url, params=parameters)

        print(r.url)

        print r.content

    @staticmethod
    def __construct_parameters(qq_session, qq_account, verify_code, need_input_verify_code):
        if need_input_verify_code:
            ptvfsession = HttpCookies.get_value('verifysession')
        else:
            HttpCookies.get_value('ptvfsession')

        parameters = {
            'u': qq_account.user_name,
            'p': QQEncryptor.encrypt2(qq_account, verify_code),
            'verifycode': verify_code,
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
            'login_sig': qq_session.login_sig,

            #2015-03-02 登录协议增加的参数
            'pt_uistyle': '5',
            'pt_randsalt': '0',
            'pt_vcode_v1': '0',
            'pt_verifysession_v1': ptvfsession
        }

        return parameters