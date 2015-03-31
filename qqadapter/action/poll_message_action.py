# -*- coding:utf8 -*-
__author__ = 'changyuf'

import json
import datetime
import urllib
from qqadapter.utilities.qq_encryptor import QQEncryptor
from qqadapter.utilities.utilities import HttpCookies, WebQQException
from qqadapter.core.qqconstants import QQConstants
from qqadapter.bean.qq_group import QQGroup
from qqadapter.bean.qq_message import QQMessage
from qqadapter.bean.qq_group_member import QQGroupMember
from qqadapter.module.user_module import UserModule
from qqadapter.module.chat_module import ChatModule


class PollMessageAction:
    def __init__(self, qq_session, request_session, account, store, group_module):
        self.qq_session = qq_session
        self.request_session = request_session
        self.account = account
        self.store = store
        self.group_module = group_module

        # for test
        self.chat_module = ChatModule(qq_session, request_session, account, store, group_module)

    def poll_message(self):
        response = self.__get_response()
        self.__parse_response(response)

    def __get_response(self):
        # URL_POLL_MSG
        url = "http://d.web2.qq.com/channel/poll2"

        ptwebqq = HttpCookies.get_value('ptwebqq')
        hash_value = QQEncryptor.hash(self.account.uin, ptwebqq)
        payload = json.dumps({
            "clientid": self.qq_session.client_id,
            "psessionid": self.qq_session.session_id,
            "key": 0,
            "ids": []
        })
        post_data = "r=%s&clientid=%s&psessionid=%s" % (
            urllib.quote(payload), self.qq_session.client_id, self.qq_session.session_id)
        response = self.request_session.post(url, data=post_data, headers=QQConstants.POST_HEADERS)
        print "Response for poll_message:", response.content

        return response

    def __parse_response(self, response):
        #data = json.loads(response.text, encoding='utf-8')
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
                buddy = self.store.buddy_map[str(from_uin)]
                print "好友 ", buddy.nick_name, "正在输入"
            elif poll_type == "message":
                # 好友消息
                msg = self.__parse_buddy_message(poll_data)
                new_msg = QQMessage()
                new_msg.to_user = msg.from_user
                new_msg.from_user = msg.to_user
                new_msg.message = msg.message
                new_msg.type = msg.type
                self.chat_module.send_message(new_msg)
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

    def __process_group_message(self, msg):
        group_name = msg.group.name
        if isinstance(group_name, unicode):
            group_name = group_name.encode('utf8')
        print "from group:", group_name
        print type("运动测试")
        if group_name == "运动测试":
            text = msg.message
            if isinstance(text, unicode):
                text = text.encode('utf-8')
            if text.startswith("@小秘书"):
                msg.message = "叫我干什么，我现在还没长大，什么都干不了"
                self.__reply_group_message(msg)
            #self.__reply_group_message(msg)
        if group_name == "后沙峪友瑞羽毛球群":
            text = msg.message
            if isinstance(text, unicode):
                text = text.encode('utf-8')
            if text.startswith("@小秘书"):
                msg.message = "叫我干什么，我现在还没长大，什么都干不了"
                self.__reply_group_message(msg)


    def __reply_group_message(self,msg):
        new_msg = QQMessage()
        new_msg.to_user = msg.from_user
        new_msg.from_user = msg.to_user
        new_msg.message = msg.message
        new_msg.group = msg.group
        new_msg.type = QQMessage.Type.GROUP_MSG
        self.chat_module.send_message(new_msg)



if __name__ == "__main__":
    text = {"retcode": 0,
                "result":
                    [{"poll_type": "group_message",
                      "value":
                          {"msg_id": 63178, "from_uin": 109394525, "to_uin": 3047296752,
                           "msg_id2": 586542, "msg_type": 43, "reply_ip": 180061927,
                           "group_code": 1220611493, "send_uin": 2301259461, "seq": 15,
                           "time": 1427704997, "info_seq": 431580233,
                           "content": [["font",
                                        {"size": 10,
                                         "color": "000000",
                                         "style": [
                                             0, 0,
                                             0],
                                         "name": "\u5B8B\u4F53"}],
                                       "hi "]}}]}
    data = json.loads(text, encoding='utf-8')




