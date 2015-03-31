# -*- coding:utf8 -*-
__author__ = 'changyuf'

import json
import random
import urllib
from qqadapter.bean.qq_message import QQMessage
from qqadapter.core.qqconstants import QQConstants
from qqadapter.utilities.utilities import HttpCookies

# MSG_FONT = {
#     'name': '微软雅黑',
#     'size': '10',
#     'style': [0, 0, 0],
#     'color': '000000'
# }
MSG_FONT = '[\"font\",{\"name\":\"宋体\",\"size\":10,\"style\":[0,0,0],\"color\":\"000000\"}]'


class ChatModule:
    def __init__(self, qq_session, request_session, account, store, group_module):
        self.qq_session = qq_session
        self.request_session = request_session
        self.account = account
        self.store = store
        self.group_module = group_module

    def send_message(self, message):
        if message.type == QQMessage.Type.SESSION_MSG:
            pass
            # final ProcActionFuture future = new ProcActionFuture(listener, true);
        # QQStranger stranger = (QQStranger) msg.getTo();
        # //			if(stranger.getGroupSig() == null || stranger.getGroupSig().equals("")) {
        # getSessionMsgSig(stranger, new QQActionListener() {
        # @Override
        # public void onActionEvent(QQActionEvent event) {
        # if(event.getType() == QQActionEvent.Type.EVT_OK) {
        # if(!future.isCanceled()){
        # doSendMsg(msg, future);
        # 							}
        # 						}else if(event.getType() == QQActionEvent.Type.EVT_ERROR){
        # 							future.notifyActionEvent(event.getType(), event.getTarget());
        # 						}
        # 					}
        # 				});
        # //			}
        # 			return future;
        elif message.type == QQMessage.Type.GROUP_MSG or message.type == QQMessage.Type.DISCUZ_MSG:
            pass
        # if(getContext().getSession().getCfaceKey() == null || getContext().getSession().getCfaceKey().equals("")) {
        # final ProcActionFuture future = new ProcActionFuture(listener, true);
        # getCFaceSig(new QQActionListener() {
        #
        # @Override
        # public void onActionEvent(QQActionEvent event) {
        # if(event.getType() == QQActionEvent.Type.EVT_OK) {
        # if(!future.isCanceled()){
        # doSendMsg(msg, future);
        # }
        # 			}else if(event.getType() == QQActionEvent.Type.EVT_ERROR){
        # 				future.notifyActionEvent(event.getType(), event.getTarget());
        # 			}
        # 		}
        # 	});
        # 	return future;
        # }

        return self.__do_send_message(message)

    def __do_send_message(self, message):
        url = "http://d.web2.qq.com/channel/poll2"

        # ptwebqq = HttpCookies.get_value('ptwebqq')
        # hash_value = QQEncryptor.hash(self.account.uin, ptwebqq)
        text = message.message
        if isinstance(text, unicode):
            text = text.encode('utf8')
        #content = [text.replace('"', '\\"'), ["font", MSG_FONT]]
        #text = '\"' + text + '\"'
        #content = "[%s, MSG_FONT]" % text
        #content = '[\"$s\",[\"font\",{\"name\":\"宋体\",\"size\":10,\"style\":[0,0,0],\"color\":\"000000\"}]]' % text
        #content = '[\\"%s\\",[\\"font\\",{\\"name\\":\\"宋体\\",\\"size\\":10,\\"style\\":[0,0,0],\\"color\\":\\"000000\\"}]]' % "无语"
        #print "content:", content
        #text = "中国好\\n市民"

        #{"to":2754143906,"content":"[\"hi\",[\"font\",{\"name\":\"宋体\",\"size\":10,\"style\":[0,0,0],\"color\":\"000000\"}]]","face":558,"clientid":53999199,"msg_id":68900001,"psessionid":"8368046764001d636f6e6e7365727665725f77656271714031302e3133392e372e31363400002a8d00000143036e0400f00ea2b56d0000000a40315872377232714c646d00000028ac8fad9c82e24709d6a606cb2388fda292f49d8e7f73a36457414274a4d55f36dd204f1f704845be"}
        payload = {
            #"content": content,
            #"content": '[\"无语\",[\"font\",{\"name\":\"宋体\",\"size\":10,\"style\":[0,0,0],\"color\":\"000000\"}]]',
            "content": '[\"%s\",[\"font\",{\"name\":\"宋体\",\"size\":10,\"style\":[0,0,0],\"color\":\"000000\"}]]' % text,
            #"content":['\"hi\"',['\"font'\"',{'\"name\"':'\"宋体\"'','\"size\"'':10,'\"style\"'':[0,0,0],'\"color\"'':'\"000000\"'}]]
            #"content": ['\"hi\"'],
            #"content":[\\"hi\",[\\"font\\",{\\"name\\":\\u"宋体\",\\"size\\":10,\\"style\\":[0,0,0],\"color\":\"000000\"}]]
            "msg_id": random.randint(10000000, 99999999),
            "clientid": self.qq_session.client_id,
            "psessionid": self.qq_session.session_id
        }

        if message.type == QQMessage.Type.BUDDY_MSG:
            # URL_SEND_BUDDY_MSG
            url = "http://d.web2.qq.com/channel/send_buddy_msg2"
            payload["to"] = int(message.to_user.uin)
            payload["face"] = 558
        elif message.type == QQMessage.Type.GROUP_MSG:
            # URL_SEND_GROUP_MSG
            url = "http://d.web2.qq.com/channel/send_qun_msg2"
            payload["group_uin"] = message.group.gin
            payload["face"] = 558
        # json.put("key", session.getCfaceKey());
        # json.put("sig", session.getCfaceSig());
        elif message.type == QQMessage.Type.DISCUZ_MSG:
            pass
        # req = createHttpRequest("POST", QQConstants.URL_SEND_DISCUZ_MSG);
        # json.put("did", msg.getDiscuz().getDid());
        # json.put("key", session.getCfaceKey());
        # json.put("sig", session.getCfaceSig());
        elif message.type == QQMessage.Type.SESSION_MSG:  # 临时会话消息
            pass
            # req = createHttpRequest("POST", QQConstants.URL_SEND_SESSION_MSG);
            # QQStranger member =  (QQStranger) msg.getTo();
            # json.put("to", member.getUin());
            # json.put("face", 0); // 这个是干嘛的？？
            # json.put("group_sig", member.getGroupSig());
            # json.put("service_type", member.getServiceType() + "");
        else:
            print "unknown MsgType: ", message.type

        json_data = json.dumps(payload)
        post_data = "r=%s&clientid=%s&psessionid=%s" % (
            urllib.quote(json_data), self.qq_session.client_id, self.qq_session.session_id)

        print "post_data:", post_data
        # post_data = data = {"r": json.dumps(payload)}
        response = self.request_session.post(url, data=post_data, headers=QQConstants.POST_HEADERS)
        #print "cookies:"
        #HttpCookies.dump(self.request_session.cookies)
        #print "\n"
        print "Response for __do_send_message:", response.content
