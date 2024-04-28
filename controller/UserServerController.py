import sys
import time


sys.path.append("../")

from model.CommonDb import *
import datetime
from frameworks.utils.ApiUtil import *

class UserServerController:
    def __init__(self):
        pass

    def adduserServerStatus(self, status_data):
        model = CommonDb('user')
        consequence = model.selectAll(f"username='{status_data['username']}' and password='{status_data['password']}'")
        if consequence:
            result = False
            print('已有此用户，无法添加')
        else:
            result = model.add(status_data)
        return result

    def findloginServerStatus(self, status_data):
        model = CommonDb('user')
        consequence = model.selectAll(f"username='{status_data['username']}' and password='{status_data['password']}'")
        if not consequence:
            result = False
            print('无此项')
        else:
            result = True
        return result

