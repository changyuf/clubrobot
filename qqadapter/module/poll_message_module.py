# -*- coding:utf8 -*-
__author__ = 'changyuf'

import json
import urllib
import logging
from qqadapter.utilities.qq_encryptor import QQEncryptor
from qqadapter.utilities.utilities import WebQQException

class PollMessageModule:
    def __init__(self, context):
        self.context = context

    def poll_message(self):
        response = self.__get_response()
        self.__parse_response(response)

    def __get_response(self):
        # URL_POLL_MSG
        url = "http://d.web2.qq.com/channel/poll2"

        ptwebqq = self.context.httpService.get_cookie_value('ptwebqq')
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
            raise WebQQException("get_group_list failed")
        logging.info("response of POLL_MESSAGE:%s", response.content)

        return response

    def __parse_response(self, response):
        data = response.json()
        if data["retcode"] != 0:
            print "get group list failed.", data["retcode"], data["errmsg"]
            return False

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
                self.__process_group_message(msg)
            elif poll_type == "discu_message":
                # 讨论组消息
                pass
                # notifyEvents.add(processDiscuzMsg(poll_data));
            elif poll_type == "sess_message":
                # 临时会话消息
                pass
                # notifyEvents.add(processSessionMsg(poll_data));
            elif poll_type == "shake_message":
                # 窗口震动
                pass
                # long fromUin = poll_data["from_uin");
                # QQUser user = getContext().getStore().getBuddyByUin(fromUin);
                # notifyEvents.add(new QQNotifyEvent(QQNotifyEvent.Type.SHAKE_WINDOW, user));
            elif poll_type == "kick_message":
                # 被踢下线
                pass
                # getContext().getAccount().setStatus(QQStatus.OFFLINE);
                # getContext().getSession().setState(QQSession.State.KICKED);
                # notifyEvents.add(new QQNotifyEvent(
                # QQNotifyEvent.Type.KICK_OFFLINE, poll_data
                # .getString("reason")));
            elif poll_type == "buddies_status_change":
                pass
                # notifyEvents.add(processBuddyStatusChange(poll_data));
            elif poll_type == "system_message":
                # 好友添加
                pass
                # QQNotifyEvent processSystemMessage = processSystemMsg(poll_data);
                # if(processSystemMessage != null){
                # notifyEvents.add(processSystemMessage);
                # }
            elif poll_type == "group_web_message":
                # 发布了共享文件
                pass

                # QQNotifyEvent processSystemMessage = processGroupWebMsg(poll_data);
                # if(processSystemMessage != null){
                # notifyEvents.add(processSystemMessage);
                # }
            elif poll_type == "sys_g_msg":
                # 被踢出了群
                pass
                # QQNotifyEvent processSystemMessage = processSystemGroupMsg(poll_data);
                # if(processSystemMessage != null){
                # notifyEvents.add(processSystemMessage);
                # }
            else:
                # 未知消息类型
                pass

            if msg:
                msg.dump()

    def __parse_buddy_message(self, poll_data):
        from_uin = str(poll_data["from_uin"])
        if not self.store.buddy_map.get(from_uin):  # 消息来自陌生人
            # QQUser member = store.getStrangerByUin(fromUin); # 搜索陌生人列表
            # if (member == null) {
            # member = new QQHalfStranger();
            # member.setUin(fromUin);
            # store.addStranger((QQStranger) member);
            #
            # # 获取用户信息
            # UserModule userModule = getContext().getModule(QQModule.Type.USER);
            #     userModule.getUserInfo(member, null);
            # }
            # msg.setFrom(member);
            return None

        msg = QQMessage()
        msg.id = poll_data["msg_id"]
        msg.id2 = poll_data["msg_id2"]
        # msg.content_list = poll_data["content"]
        # msg.parseContentList(poll_data.getJSONArray("content").toString());
        msg.parse_content_list(poll_data["content"])
        msg.type = QQMessage.Type.BUDDY_MSG
        msg.to_user = self.account
        msg.from_user = self.store.buddy_map[from_uin]
        msg.time = datetime.datetime.fromtimestamp(poll_data["time"])

        return msg

    def __parse_group_message(self, poll_data):
        msg = QQMessage()
        msg.id = poll_data["msg_id"]
        msg.id2 = poll_data["msg_id2"]
        from_uin = str(poll_data["send_uin"])
        group_code = poll_data["group_code"]
        group_id = poll_data["info_seq"];  # 真实群号码
        group = self.store.group_map.get(group_code)
        if not group:
            group = QQGroup()
            group.code = group_code
            group.gid = group_id
            # put to store
            self.store.add_group(group)
            self.group_module.get_group_info(group)
        if group.gid <= 0:
            group.gid = group_id

        #msg.content_list = poll_data["content"]
        msg.parse_content_list(poll_data["content"])
        msg.type = QQMessage.Type.GROUP_MSG
        msg.group = group
        msg.to_user = self.account
        msg.time = datetime.datetime.fromtimestamp(poll_data["time"])
        msg.from_user = group.get_member_by_uin(from_uin)
        if not msg.from_user:
            member = QQGroupMember()
            member.uin = from_uin
            msg.from_user = member
            group.members.append(member)

            UserModule.get_stranger_info(self.qq_session, member, self.request_session)

        return msg
