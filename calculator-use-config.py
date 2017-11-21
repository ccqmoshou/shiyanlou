#!/usr/bin/python3

import sys

class Config(object):
    def __init__(self, configfile):
        self.config = self.read_config()

    def read_config(self):
        config = {}
        with open(configfile) as f:
            for line in f.readlines():
                key, value = line.strip().split(' = ')
                try:
                    config[key] = float(value)
                except:
                    print("Parameter Error")
                    exit()
        return config

    def get_config(self, key):
        try:
            return self.config[key]
        except:
            print("Config Error")
            exit()   

    def social_high_baseline(self):
        return self.get_config("JiShuH")

    def social_low_baseline(self):
        return self.get_config("JiShuL")

    def social_total_rate(self):
        return sum([self.get_config("YangLao"), self.get_config("YiLiao"), self.get_config("ShiYe"), self.get_config("GongShang"), self.get_config("ShengYu"), self.get_config("GongJiJin")])


class UserData(object):
    def __init__(self, userdatafile):
        self.userdata = self.read_userdata()

    def read_userdata(self):
        userdata = {}
        with open(userdatafile) as f:
            for line in f.readlines():
                key, value = line.strip().split(',')
                try:
                    userdata[key] = int(value)
                except:
                    print("Parameter Error")
                    exit()
        return userdata

    def get_user(self, key):
        return self.userdata[key]


