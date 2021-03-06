# -*- coding:utf8 -*-
__author__ = 'changyuf'

import json
import random
import urllib
import logging
from qqadapter.bean.qq_message import QQMessage
from qqadapter.core.qqconstants import QQConstants
from qqadapter.utilities.utilities import WebQQException

# MSG_FONT = {
#     'name': '微软雅黑',
#     'size': '10',
#     'style': [0, 0, 0],
#     'color': '000000'
# }
MSG_FONT = '[\"font\",{\"name\":\"宋体\",\"size\":10,\"style\":[0,0,0],\"color\":\"000000\"}]'


class ChatModule:
    def __init__(self, context):
        self.context = context

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
        # ptwebqq = HttpCookies.get_value('ptwebqq')
        # hash_value = QQEncryptor.hash(self.account.uin, ptwebqq)
        text = message.message
        if isinstance(text, unicode):
            text = text.encode('utf8')
        text.replace('"', '\\"')

        #{"to":2754143906,"content":"[\"hi\",[\"font\",{\"name\":\"宋体\",\"size\":10,\"style\":[0,0,0],\"color\":\"000000\"}]]","face":558,"clientid":53999199,"msg_id":68900001,"psessionid":"8368046764001d636f6e6e7365727665725f77656271714031302e3133392e372e31363400002a8d00000143036e0400f00ea2b56d0000000a40315872377232714c646d00000028ac8fad9c82e24709d6a606cb2388fda292f49d8e7f73a36457414274a4d55f36dd204f1f704845be"}
        payload = {
            "content": '[\"%s\",[\"font\",{\"name\":\"宋体\",\"size\":10,\"style\":[0,0,0],\"color\":\"000000\"}]]' % text,
            "msg_id": random.randint(10000000, 99999999),
            "clientid": self.context.qq_session.client_id,
            "psessionid": self.context.qq_session.session_id
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
        elif message.type == QQMessage.Type.DISCUZ_MSG:
            return True
        # req = createHttpRequest("POST", QQConstants.URL_SEND_DISCUZ_MSG);
        # json.put("did", msg.getDiscuz().getDid());
        # json.put("key", session.getCfaceKey());
        # json.put("sig", session.getCfaceSig());
        elif message.type == QQMessage.Type.SESSION_MSG:  # 临时会话消息
            return True
            # req = createHttpRequest("POST", QQConstants.URL_SEND_SESSION_MSG);
            # QQStranger member =  (QQStranger) msg.getTo();
            # json.put("to", member.getUin());
            # json.put("face", 0); // 这个是干嘛的？？
            # json.put("group_sig", member.getGroupSig());
            # json.put("service_type", member.getServiceType() + "");
        else:
            print "unknown MsgType: ", message.type
            return True

        json_data = json.dumps(payload)
        post_data = "r=%s&clientid=%s&psessionid=%s" % (
            urllib.quote(json_data), self.context.qq_session.client_id, self.context.qq_session.session_id)

        logging.debug("send message.post_data: %s", post_data)
        response = self.context.http_service.post(url, post_data)
        if not response:
            raise WebQQException("send message failed")
        logging.info("response of SEND_MESSAGE:%s", response.content)
