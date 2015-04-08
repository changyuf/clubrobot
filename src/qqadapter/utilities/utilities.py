# -*- coding:utf8 -*-
__author__ = 'changyuf'

import cookielib


def to_str(s):
    if isinstance(s, unicode):
        return s.encode('utf8')
    return s


def transfer_gender(gender):
    gender = to_str(gender)
    if gender == "female":
        return "女"
    if gender == "male":
        return "男"
    return "人妖"


class WebQQException(Exception):
    pass


# class HttpCookies:
#     cookie_jar = cookielib.LWPCookieJar(filename="./http_cookies.txt")
#
#     def __init__(self):
#         pass
#
#     @staticmethod
#     def save_cookies(cookie_jar):
#         for c in cookie_jar:
#             args = dict(vars(c).items())
#             args['rest'] = args['_rest']
#             del args['_rest']
#             c = cookielib.Cookie(**args)
#             HttpCookies.cookie_jar.set_cookie(c)
#
#         HttpCookies.cookie_jar.save(ignore_discard=True)
#
#     @staticmethod
#     def save_cookies_lwp(cookie_jar):
#         HttpCookies.cookie_jar = cookie_jar
#         lwp_cookie_jar = cookielib.LWPCookieJar()
#         for c in cookie_jar:
#             args = dict(vars(c).items())
#             args['rest'] = args['_rest']
#             del args['_rest']
#             c = cookielib.Cookie(**args)
#             lwp_cookie_jar.set_cookie(c)
#         lwp_cookie_jar.save(HttpCookies.file_name, ignore_discard=True)
#
#     @staticmethod
#     def load_cookies_from_lwp():
#         lwp_cookie_jar = cookielib.LWPCookieJar()
#         lwp_cookie_jar.load(HttpCookies.filen_ame, ignore_discard=True)
#         return lwp_cookie_jar
#
#     @staticmethod
#     def get_value(name):
#         for cookie in HttpCookies.cookie_jar:
#             if cookie.name == name:
#                 return cookie.value
#
#         return None
#
#     @staticmethod
#     def dump(cookies=None):
#         if not cookies:
#             cookies = HttpCookies.cookie_jar
#         for cookie in cookies:
#             print "key:%s\t value:%s" % (cookie.name, cookie.value)