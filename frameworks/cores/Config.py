import configparser
import os
import socket
import platform

class Config:
    conf = ""

    def __init__(self):
        sys_platform = platform.platform().lower()
        print(sys_platform)
        if "windows" in sys_platform:
            cfgpath = "E:\\Python\\project\\Vivo_AIGC\\aigc_api_test\\configs\\machine.ini"
        else:
            cfgpath = "/root/python/code/config/userserver_config.ini"

        # 创建管理对象
        self.conf = configparser.ConfigParser()

        # 读ini文件
        self.conf.read(cfgpath, encoding="utf-8")  # python3

    def getDB(self):
        return [self.conf.get("api_vivo_project", "host"),
                self.conf.get("api_vivo_project", "user"),
                self.conf.get("api_vivo_project", "pass"),
                self.conf.getint("api_vivo_project", "port"),
                self.conf.get("api_vivo_project", "dbname")
                ]

    def getOcsOnline(self):
        return [self.conf.get("ocs_online","host"),
                self.conf.get("ocs_online","user"),
                self.conf.get("ocs_online","pass"),
                self.conf.getint("ocs_online","port"),
                self.conf.get("ocs_online","dbname")
                ]