# -*- coding:utf8 -*-
__author__ = 'changyuf'

import logging
import time
import json
import urllib
from qqadapter.utilities.qq_encryptor import QQEncryptor
from qqadapter.utilities.utilities import WebQQException, to_str, transfer_gender
from qqadapter.bean.qq_group import QQGroup
from qqadapter.bean.qq_group_member import QQGroupMember


# 群模块，处理群相关操作
class GroupModule:
    def __init__(self, context):
        self.context = context

    # 获取群列表
    def get_group_list(self):
        # URL_GET_GROUP_NAME_LIST
        url = "http://s.web2.qq.com/api/get_group_name_list_mask2"

        ptwebqq = self.context.http_service.get_cookie_value('ptwebqq')
        hash_value = QQEncryptor.hash(self.context.account.uin, ptwebqq)
        payload = json.dumps({
            "vfwebqq": self.context.qq_session.vfwebqq,
            "hash": hash_value,
        })
        post_data = "r=%s" % urllib.quote(payload)
        response = self.context.http_service.post(url, post_data)
        if not response:
            raise WebQQException("get_group_list failed")
        logging.info("response of GET_GROUP_LIST:%s", response.content)

        data = json.loads(response.text, encoding='utf-8')
        if data["retcode"] != 0:
            logging.error("get group list failed.retcode:%s,errmsg:%s", (data["retcode"], data.get("errmsg")))
            return False

        results = data["result"]
        group_list = results["gnamelist"]  # 群列表
        group_mask_list = results["gmasklist"]  # 禁止接收群消息标志：正常 0， 接收不提醒 1， 完全屏蔽 2
        for g in group_list:
            group = QQGroup()
            group.gin = g['gid']
            group.code = g["code"]
            group.flag = g["flag"]
            group.name = to_str(g['name'])
            self.context.store.add_group(group)

        for mask in group_mask_list:
            gid = mask['gid']
            mask = mask['mask']
            group = self.context.store.get_group_by_gin(gid)
            if group:
                group.mask = mask

        return True

    def get_group_info(self, group):
        # URL_GET_GROUP_INFO_EXT
        url = "http://s.web2.qq.com/api/get_group_info_ext2"
        parameters = {
            'gcode': group.code,
            'vfwebqq': self.context.qq_session.vfwebqq,
            't': str(int(time.time()))
        }

        response = self.context.http_service.get(url, parameters)
        if not response:
            raise WebQQException("get_group_list failed")
        logging.info("response of GET_GROUP_INFO:%s", response.content)
        data = json.loads(response.text, encoding='utf-8')

        if not data:
            logging.error("get_group_info failed.there is no json data return.")
            return False

        if data["retcode"] != 0:
            logging.error("get group info failed.retcode:%s,errmsg:%s", (data["retcode"], data.get("errmsg")))
            return False

        results = data["result"]
        GroupModule.parse_group_info(results, group)

        return True

    @staticmethod
    def parse_group_info(results, group):
        ginfo = results["ginfo"]
        group.memo = ginfo.get("memo")
        group.level = ginfo.get("level")

        members = ginfo.get("members")
        for memjson in members:
            uin = str(memjson.get("muin"))
            member = group.get_member_by_uin(uin);
            if not member:
                member = QQGroupMember()
                group.members.append(member)
            member.uin = uin
            member.group = group

        # result/minfo
        minfos = results["minfo"]
        for minfo in minfos:
            uin = str(minfo.get("uin"))
            member = group.get_member_by_uin(uin)
            member.nick_name = to_str(minfo.get("nick"))
            member.province = to_str(minfo.get("province"))
            member.country = to_str(minfo.get("country"))
            member.city = to_str(minfo.get("city"))
            member.gender = transfer_gender(minfo.get("gender"))

        cards = results.get("cards")
        if cards:
            for card in cards:
                muin = str(card.get("muin"))
                member = group.get_member_by_uin(muin)
                member.card = to_str(card.get("card"))

        return True

