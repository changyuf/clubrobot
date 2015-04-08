# -*- coding:utf8 -*-
__author__ = 'changyuf'

import os
import ConfigParser
from robot.utility.singleton import Singleton


class Config(Singleton):
    def __init__(self):
        self.cf = ConfigParser.ConfigParser()
        config_file = os.getenv("CONFIG_FILE", os.path.join(os.getcwd(), "config", "club_robot.conf"))
        self.cf.read(config_file)
        self.test = 1

    def get(self, section, option):
        return self.cf.get(section, option)


if __name__ == "__main__":
    config = Config()
    config2 = Config()
    config.test = 2
    print config2.test
    config2.test = 100
    print config.test

    print config == config2

    print config.get("db", "db_host")
    print config.get("db", "db_user")
    print config.get("db", "db_pass")
    print config.get("db", "data_base")
    print config.get("robot", "log_file")
    group_name = config.get("robot", "group_name")
    print group_name
    print group_name == "后沙峪友瑞羽毛球群"




