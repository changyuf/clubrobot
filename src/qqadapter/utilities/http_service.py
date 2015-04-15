# -*- coding:utf8 -*-
__author__ = 'changyuf'

import logging
import requests
from qqadapter.core.qqconstants import QQConstants


class HttpService:
    def __init__(self):
        self.session = requests.session()

    def get(self, url, parameters=None, header=QQConstants.GET_HEADERS):
        # if not header:
        # header = QQConstants.GET_HEADERS

        try:
            response = self.session.get(url, params=parameters, headers=header)
            if response.status_code != 200:
                logging.error("Get data failed. URL: %s", url)
                return None
        except requests.exceptions.RequestException:
            logging.exception("Get data failed. URL:%s", url)
            return None

        return response

    def post(self, url, post_data=None, header=QQConstants.POST_HEADERS):
        try:
            response = self.session.post(url, data=post_data, headers=header)
            if response.status_code != 200:
                logging.error("Get data failed. URL: %s", url)
                return None
        except requests.exceptions.RequestException:
            logging.exception("Get data failed. URL: %s", url)
            return None

        return response

    def get_cookie_value(self, key):
        dct = self.session.cookies.get_dict()
        return dct.get(key)



