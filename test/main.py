# -*- coding:utf8 -*-
__author__ = 'changyuf'

from qqadapter.qqclient import QQClient
import sys
import os
import platform
import random
import datetime
import requests
import re

from qqadapter.core.qqconstants import QQConstants

if __name__ == "__main__":
    try:
        f = open("user.txt")
        user = f.readline()
        password = f.readline()
    except IOError:
        user = '2899530487'
        password = 'bbb'

    # print user, password

    #print Constants.USER_AGENT
    url = QQConstants.URL_CHECK_VERIFY.format(user, 'WKopqcbLJTQ1fs*AO3JW8IBqC*x5E8ICrner0obUGL6arpF68F8CGTsva8iu54Yd',
                                            random.random())

    print "url:" + url
    print

    url = QQConstants.URL_LOGIN_PAGE
    s = requests.session()
    r = s.get(url, headers=QQConstants.HEADERS)
    #r = requests.get(url, headers=Constants.HEADERS)

    #if r.headers :
    #    print r.headers

    print r.content

    #m = re.match(Constants.REGXP_LOGIN_SIG, r.content)
    m = re.search(QQConstants.REGXP_LOGIN_SIG, r.content)
    if m:
        print "log_sig:" + m.group(1)
    else:
        print "did not find log_sig"


    #print r.raw
    #print r.cookies

    #print r

    #print s.cookies
    #print s.params
    #print r

    # print datetime.datetime.now().


    #print Constants.HEADERS['User-Agent']
    exit()

    # qq = QqClient(user, password)
    #print sys.platform
    #print sys.version
    print platform.system()
    print platform.platform()  #获取操作系统名称及版本号，'Windows-7-6.1.7601-SP1'
    print platform.version()  #获取操作系统版本号，'6.1.7601'
    print platform.architecture()  #获取操作系统的位数，('32bit', 'WindowsPE')
    print platform.machine()  #计算机类型，'x86'
    #print platform.node()       #计算机的网络名称，'hongjie-PC'
    #print platform.processor()  #计算机处理器信息，'x86 Family 16 Model 6 Stepping 3, AuthenticAMD'
    print platform.uname()

    exit()
    s = 'name is {first} {second}'
    person = {'first': 'aa', 'second': 'bb', 'third': 'ooo'}
    template = '''name is %(first)s %(third)s'''
    s = template % person
    # s = s.format(person)
    print s

    print "奉昌玉"