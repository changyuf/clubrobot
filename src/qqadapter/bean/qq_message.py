# -*- coding:utf8 -*-
__author__ = 'changyuf'

import json
from enum import Enum
from qqadapter.bean.qquser import QQUser


class QQMessage:
    def __init__(self):
        self.id = 0  # 消息ID
        self.id2 = 0  # 暂时不知什么含义
        self.type = QQMessage.Type.BUDDY_MSG  # 消息类型
        self.to_user = None  # 消息发送方
        self.from_user = None  # 消息发送方
        self.group = None  # 所在群
        self.discuz = None  # 讨论组
        self.time = None  # 发送时间
        # self.content_list = None  # 消息列表
        self.message = ""

    def parse_content_list(self, text):
        # text is in format [[u'font', {u'color': u'000000', u'style': [0, 0, 0], u'name': u'\u5b8b\u4f53', u'size': 10}], [u'face', 13], u'\u6d4b\u8bd5', [u'face', 13], u' ']
        for data in text:
            if isinstance(data, unicode):
                self.message += data.encode("utf-8")
            elif isinstance(data, str):
                self.message += data

        return True

    # for (int i = 0; i < json.length(); i++) {
    # Object value = json.get(i);
    # if(value instanceof JSONArray){
    # 		JSONArray items = (JSONArray) value;
    # 		ContentItem.Type type = ContentItem.Type.valueOfRaw(items.getString(0));
    # 		switch (type) {
    # 			case FACE:    addContentItem(new FaceItem(items.toString())); break;
    # 			case FONT:    addContentItem(new FontItem(items.toString())); break;
    # 			case CFACE:   addContentItem(new CFaceItem(items.toString())); break;
    # 			case OFFPIC: addContentItem(new OffPicItem(items.toString())); break;
    # 			default:
    # 		}
    # 	}else if( value instanceof String){
    # 		addContentItem(new TextItem((String) value));
    # 	}else{
    # 		throw new QQException(QQErrorCode.UNKNOWN_ERROR, "unknown msg content type:" + value.toString());
    # 	}
    # }

    def dump(self):
        if self.id:
            print "id:", self.id
        if self.id2:
            print "id2:", self.id2
        if self.type:
            print "type:", self.type.name
        if self.to_user:
            print "to user:", self.to_user.nick_name
        if self.from_user:
            print "from user:", self.from_user.nick_name
        if self.group:
            print "from group:", self.group.name
        if self.message:
            print "message:", self.message

    class Type(Enum):
        BUDDY_MSG = 0  # 好友消息
        GROUP_MSG = 1  # 群消息
        DISCUZ_MSG = 2  # 讨论组消息
        SESSION_MSG = 3  # 临时会话消息


if __name__ == '__main__':
    msg = QQMessage()
    msg.id = 1
    msg.id2 = 2
    msg.type = QQMessage.Type.BUDDY_MSG
    user1 = QQUser()
    user1.nick_name = "nick name 1"
    user2 = QQUser()
    user2.nick_name = "nick name 2"

    msg.to_user = user1
    msg.from_user = user2
    msg.message = "我是消息"
    msg.dump()

    # text = [[u'font', {u'color': u'000000', u'style': [0, 0, 0], u'name': u'\u5b8b\u4f53', u'size': 10}], u'\u6d4b\u8bd5 ']
    text = [[u'font', {u'color': u'000000', u'style': [0, 0, 0], u'name': u'\u5b8b\u4f53', u'size': 10}], [u'face', 13],
            u'\u6d4b\u8bd5', [u'face', 13], u' ']
    for item in text:
        # data = json.dump(item)
        #print type(item)
        if isinstance(item, unicode):
            item = item.encode("utf-8")
            #print type(item)
            print item
            # print text.encode('utf-8')
