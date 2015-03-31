# -*- coding:utf8 -*-
__author__ = 'changyuf'

import platform


class QQConstants:
    USER_AGENT = "Mozilla/5.0 (%(os_platform)s; %(os_arch)s) AppleWebKit/537.36 (KHTML, like Gecko)  IQQ Client/1.2 dev Safari/537.36" % {
        'os_platform': platform.platform(), 'os_arch': platform.machine()}

    #REFFER = "http://d.web2.qq.com/proxy.html?v=20140612002&callback=1&id=3"
    REFFER = "http://d.web2.qq.com/proxy.html?v=20130916001&callback=1&id=2"

    APPID = "1003903"

    JSVER = "10114"

    URL_LOGIN_PAGE = "https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&target=self&style=5&mibao_css=m_webqq&appid=" + APPID + "&enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fweb2.qq.com%2Floginproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20140612002"

    URL_CHECK_VERIFY = "https://ssl.ptlogin2.qq.com/check?pt_tea=1&uin={0}&appid=" + APPID + "&js_ver=10114&js_type=0&login_sig={1}&u1=http%3A%2F%2Fweb2.qq.com%2Floginproxy.html&r={2}"

    GET_HEADERS = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'utf-8',
        'User-Agent': USER_AGENT,
        "Referer": REFFER
    }

    POST_HEADERS = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate,sdch",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        #"Content-type": "application/x-www-form-urlencoded",
        "Content-type":"application/x-www-form-urlencoded; charset=UTF-8",
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Referer": REFFER
    }

