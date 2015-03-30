# -*- coding:utf8 -*-
__author__ = 'changyuf'

import json
import urllib
from qqadapter.utilities.qq_encryptor import QQEncryptor
from qqadapter.utilities.utilities import HttpCookies,WebQQException
from qqadapter.core.qqconstants import QQConstants
from qqadapter.bean.qq_group import QQGroup


# 群模块，处理群相关操作
class GroupModule:
    def __init__(self, qq_session, request_session, account, store):
        self.qq_session = qq_session
        self.request_session = request_session
        self.account = account
        self.store = store

    # 获取群列表
    def get_group_list(self):
        # URL_GET_GROUP_NAME_LIST
        url = "http://s.web2.qq.com/api/get_group_name_list_mask2"

        ptwebqq = HttpCookies.get_value('ptwebqq')
        hash_value = QQEncryptor.hash(self.account.uin, ptwebqq)
        payload = json.dumps({
            "vfwebqq": self.qq_session.vfwebqq,
            "hash": hash_value,
        })
        post_data = "r=%s" % urllib.quote(payload)
        response = self.request_session.post(url,  data=post_data, headers=QQConstants.POST_HEADERS)
        print response.content

        data = json.loads(response.text, encoding='utf-8')
        if data["retcode"] != 0:
            print "get group list failed.", data["retcode"], data["errmsg"]
            return False

        results = data["result"]
        group_list = results["gnamelist"]	 # 群列表
        group_mask_list = results["gmasklist"]  # 禁止接收群消息标志：正常 0， 接收不提醒 1， 完全屏蔽 2
        for g in group_list:
            group = QQGroup()
            group.gin = g['gid']
            group.code = g["code"]
            group.flag = g["flag"]
            group.name = g['name']
            self.store.group_map[group.code] = group

        for mask in group_mask_list:
            gid = mask['gid']
            mask = mask['mask']
            group = self.store.get_group_by_gin(gid)
            if group:
                group.mask = mask

        return True
