# -*- coding:utf8 -*-
__author__ = 'changyuf'

def to_str(s):
    if isinstance(s, unicode):
        return s.encode('utf8')
    return s
