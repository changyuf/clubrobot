# -*- coding:utf8 -*-
__author__ = 'changyuf'

import time
import json
import urllib
from qqadapter.utilities.qq_encryptor import QQEncryptor
from qqadapter.utilities.utilities import HttpCookies, WebQQException
from qqadapter.core.qqconstants import QQConstants
from qqadapter.bean.qq_group import QQGroup
from qqadapter.bean.qq_group_member import QQGroupMember


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
        response = self.request_session.post(url, data=post_data, headers=QQConstants.POST_HEADERS)
        print response.content

        data = json.loads(response.text, encoding='utf-8')
        if data["retcode"] != 0:
            print "get group list failed.", data["retcode"], data["errmsg"]
            return False

        results = data["result"]
        group_list = results["gnamelist"]  # 群列表
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

    def get_group_info(self, group):
        # URL_GET_GROUP_INFO_EXT
        url = "http://s.web2.qq.com/api/get_group_info_ext2"
        parameters = {
            'gcode': group.code,
            'vfwebqq': self.qq_session.vfwebqq,
            't': str(int(time.time()))
        }

        response = self.requests_session.get(url, headers=QQConstants.GET_HEADERS, params=parameters)
        print response
        data = json.loads(response.text, encoding='utf-8')
        if data["retcode"] != 0:
            print "get group list failed.", data["retcode"], data["errmsg"]
        return False

        results = data["result"]
        self.__parse_grouop_info_response(results, group)

        return True

    def __parse_group_info_response(self, results, group):
        ginfo = results["ginfo"]
        group.memo = ginfo.get("memo")
        group.level = ginfo.get("level")
        # group.setCreateTime(new Date(ginfo.getInt("createtime")));

        members = ginfo.get("members")
        for memjson in members:
            uin = str(memjson.get("muin"))
            member = group.get_member_by_uin(uin);
            if not member:
                member = QQGroupMember()
                group.members.append(member)
            member.uin = uin
            member.group = group
            # memjson.getLong("mflag");

        # result/minfo
        minfos = results["minfo"]
        for minfo in minfos:
            uin = str(minfos.get("uin"))
            member = group.get_member_by_uin(uin)
            member.setNickname(minfo.get("nick"))
            member.setProvince(minfo.get("province"))
            member.setCountry(minfo.get("country"))
            member.setCity(minfo.get("city"));
            member.setGender(minfo.get("gender"))

        return True

# // result / stats
#         JSONArray
#         stats = json.getJSONArray("stats");
#         for (int i=0; i < stats.length(); i++){
#         // 下面重新设置最新状态
#         JSONObject
#         stat = stats.getJSONObject(i);
#         QQGroupMember
#         member = group.getMemberByUin(stat.getLong("uin"));
#         member.setClientType(QQClientType.valueOfRaw(stat.getInt("client_type")));
#         member.setStatus(QQStatus.valueOfRaw(stat.getInt("stat")));
#
#     }
#
#     // results / cards
#     if (json.has("cards"))
#     {
#     JSONArray
#     cards = json.getJSONArray("cards");
#     for (int i=0; i < cards.length(); i++){
#     JSONObject card = cards.getJSONObject(i);
#     QQGroupMember member = group.getMemberByUin(card.getLong("muin"));
#     if ( card != null & & card.has("card") & & member != null ) {
#     member.setCard(card.get("card"));
#     }
#     }
#
# }
#
# // results / vipinfo
# JSONArray
# vipinfos = json.getJSONArray("vipinfo");
# for (int
# i = 0;
# i < vipinfos.length();
# i + +){
# JSONObject
# vipinfo = vipinfos.getJSONObject(i);
# QQGroupMember
# member = group.getMemberByUin(vipinfo.getLong("u"));
# member.setVipLevel(vipinfo.getInt("vip_level"));
# member.setVip(vipinfo.getInt("is_vip") == 1);
# }
