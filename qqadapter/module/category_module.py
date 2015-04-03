# -*- coding:utf8 -*-
__author__ = 'changyuf'

import json
import urllib
import logging
from qqadapter.utilities.qq_encryptor import QQEncryptor
from qqadapter.utilities.utilities import WebQQException
from qqadapter.bean.qq_category import QQCategory
from qqadapter.bean.qq_buddy import QQBuddy, QQUser
from qqadapter.core.qqstore import QQStore


class CategoryModule:
    def __init__(self, context):
        self.context = context

    def get_category_list(self):
        # URL_GET_USER_CATEGORIES
        url = "http://s.web2.qq.com/api/get_user_friends2"

        ptwebqq = self.context.http_service.get_cookie_value('ptwebqq')
        hash_value = QQEncryptor.hash(self.context.account.uin, ptwebqq)
        payload = json.dumps({
            "h": "hello",
            "vfwebqq": self.context.qq_session.vfwebqq,
            "hash": hash_value,
        })
        post_data = "r=%s" % urllib.quote(payload)
        response = self.context.http_service.post(url, post_data)
        if not response:
            raise WebQQException("get_group_list failed")
        logging.info("response of GET_CATEGORY_LIST:%s", response.content)

        data = json.loads(response.text)
        if data["retcode"] != 0:
            logging.error("get group category list failed.retcode:%s,errmsg:%s", (data["retcode"], data.get("errmsg")))
            return False

        # return self.parse_response(data)
        return self.parse_response(response.json())

    def parse_response(self, data):
        result = data["result"]
        categories = result["categories"]
        friends = result["friends"]
        infos = result["info"]
        mark_names = result["marknames"]
        #vip_info = result["vipinfo"]

        # 默认好友列表
        default_category = QQCategory()
        default_category.index = 0
        default_category.name = "我的好友"
        default_category.sort = 0
        self.context.store.category_map[0] = default_category

        # 初始化好友列表
        for category in categories:
            qqc = QQCategory()
            qqc.index = category["index"]
            qqc.name = category["name"]
            qqc.sort = category["sort"]
            self.context.store.category_map[qqc.index] = qqc
            print "type of name:", type(category["name"])
            print "type of qqc.name:", type(qqc.name)
            print category["name"]
            print qqc.name == u"同学"
            aaa = u"分组名:" + qqc.name + u"\n"
            print "type of aaa:", type(aaa)
            print aaa

            bbb = "bbb:%s" % qqc
            print bbb

        # 处理好友基本信息列表 flag/uin/categories
        for friend in friends:
            buddy = QQBuddy()
            buddy.uin = str(friend["uin"])
            buddy.status = QQUser.Status.OFFLINE
            # buddy.setClientType(QQClientType.UNKNOWN);
            # 添加到列表中
            category_index = friend["categories"]
            qq_category = self.context.store.category_map[category_index]
            buddy.category = qq_category
            qq_category.buddy_list.append(buddy)

            # 记录引用
            self.context.store.buddy_map[buddy.uin] = buddy

        # face/flag/nick/uin
        for info in infos:
            uin = str(info["uin"])
            buddy = self.context.store.buddy_map[uin]
            buddy.nick_name = info["nick"]
            print info["nick"]

            print buddy

        # uin/markname
        for mark in mark_names:
            uin = str(mark["uin"])
            buddy = self.context.store.buddy_map[uin]
            if buddy:
                buddy.mark_name = mark["markname"]

        return True


if __name__ == '__main__':
    data = {"retcode": 0,
            "result":
                {"friends":
                     [{"flag": 0, "uin": 3655773441, "categories": 0}], "marknames": [],
                 "categories":
                     [{"index": 1, "sort": 1, "name": "朋友".decode("utf-8")},
                      {"index": 2, "sort": 2, "name": "家人"},
                      {"index": 3, "sort": 3, "name": "同学"}],
                 "vipinfo":
                     [{"vip_level": 0, "u": 3655773441, "is_vip": 0}],
                 "info":
                     [{"face": 273, "flag": 8388608, "nick": "Test", "uin": 3655773441}]
                }
    }
    store = QQStore()
    category_module = CategoryModule(None, None, None, store)
    category_module.parse_response(data)
    store.print_category_info()




