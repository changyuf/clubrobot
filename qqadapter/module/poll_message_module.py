# -*- coding:utf8 -*-
__author__ = 'changyuf'

import json
import urllib
import logging
import datetime
from qqadapter.utilities.qq_encryptor import QQEncryptor
from qqadapter.utilities.utilities import WebQQException
from qqadapter.bean.qq_message import QQMessage
from qqadapter.bean.qq_group_member import QQGroupMember
from qqadapter.bean.qq_group import QQGroup
from qqadapter.bean.qq_stranger import QQStranger


class PollMessageModule:
    def __init__(self, context, user_module):
        self.context = context
        self.user_module = user_module

    def poll_message(self):
        response = self.__get_response()
        return self.__parse_response(response)

    def __get_response(self):
        # URL_POLL_MSG
        url = "http://d.web2.qq.com/channel/poll2"

        ptwebqq = self.context.http_service.get_cookie_value('ptwebqq')
        hash_value = QQEncryptor.hash(self.context.account.uin, ptwebqq)
        payload = json.dumps({
            "clientid": self.context.qq_session.client_id,
            "psessionid": self.context.qq_session.session_id,
            "key": 0,
            "ids": []
        })
        post_data = "r=%s&clientid=%s&psessionid=%s" % (
            urllib.quote(payload), self.context.qq_session.client_id, self.context.qq_session.session_id)

        response = self.context.http_service.post(url, post_data)
        if not response:
            raise WebQQException("poll message failed")
        logging.info("response of POLL_MESSAGE:%s", response.content)

        return response

    def __parse_response(self, response):
        data = response.json()
        if data["retcode"] == 116:
            # 需要更新ptwebqq值，暂时不知道干嘛用的
            # {"retcode":116,"p":"2c0d8375e6c09f2af3ce60c6e081bdf4db271a14d0d85060"}
            return data["retcode"], data["p"]
        if data["retcode"] != 0:
            return data["retcode"], None

        results = data["result"]
        for message in results:
            poll_type = message["poll_type"]
            poll_data = message["value"]

            msg = None
            if poll_type == "input_notify":
                from_uin = poll_data["from_uin"]
                buddy = self.context.store.buddy_map[str(from_uin)]
            elif poll_type == "message":
                # 好友消息
                msg = self.__parse_buddy_message(poll_data)
            elif poll_type == "group_message":
                # 群消息
                msg = self.__parse_group_message(poll_data)
            elif poll_type == "discu_message":
                # 讨论组消息
                logging.info("收到讨论组消息")
            elif poll_type == "sess_message":
                # 临时会话消息
                logging.info("收到临时会话消息")
            elif poll_type == "shake_message":
                # 窗口震动
                logging.info("收到窗口震动消息")
            elif poll_type == "kick_message":
                # 被踢下线
                logging.error("被踢下线")
                return 250, None
            elif poll_type == "buddies_status_change":
                pass
            elif poll_type == "system_message":
                # 好友添加
                logging.info("好友添加消息")
            elif poll_type == "group_web_message":
                # 发布了共享文件
                pass
            elif poll_type == "sys_g_msg":
                # 被踢出了群
                logging.info("好友添加消息")
            else:
                # 未知消息类型
                logging.info("未知消息类型")

            if msg:
                msg.dump()

            return data["retcode"], msg

    def __parse_buddy_message(self, poll_data):
        from_uin = str(poll_data["from_uin"])
        msg = QQMessage()
        msg.id = poll_data["msg_id"]
        msg.id2 = poll_data["msg_id2"]
        msg.parse_content_list(poll_data["content"])
        msg.type = QQMessage.Type.BUDDY_MSG
        msg.to_user = self.context.account
        msg.from_user = self.context.store.get_buddy_by_uin(from_uin)
        msg.time = datetime.datetime.fromtimestamp(poll_data["time"])

        if not msg.from_user:  # 消息来自陌生人
            member = self.context.store.get_stranger_by_uin(from_uin) # 搜索陌生人列表
            if not member:
                member = QQStranger()
                member.uin(from_uin);
                self.context.store.add_stranger(member)
                self.user_module.get_friend_info(member)
                msg.from_user = member

        return msg

    def __parse_group_message(self, poll_data):
        msg = QQMessage()
        msg.id = poll_data["msg_id"]
        msg.id2 = poll_data["msg_id2"]
        from_uin = str(poll_data["send_uin"])
        group_code = poll_data["group_code"]
        group_id = poll_data["info_seq"];  # 真实群号码
        group = self.context.store.group_map.get(group_code)
        if not group:
            group = QQGroup()
            group.code = group_code
            group.gid = group_id
            # put to store
            self.context.store.add_group(group)
            self.group_module.get_group_info(group)
        if group.gid <= 0:
            group.gid = group_id

        msg.parse_content_list(poll_data["content"])
        msg.type = QQMessage.Type.GROUP_MSG
        msg.group = group
        msg.to_user = self.context.account
        msg.time = datetime.datetime.fromtimestamp(poll_data["time"])
        msg.from_user = group.get_member_by_uin(from_uin)
        if not msg.from_user:
            member = QQGroupMember()
            member.uin = from_uin
            msg.from_user = member
            group.members.append(member)

            self.user_module.get_stranger_info( member)

        return msg
