import sys
import time


sys.path.append("../")

from model.CommonDb import *
import datetime
from frameworks.utils.ApiUtil import *

class UserServerController:
    def __init__(self):
        pass

    # def adduserServerStatus(self, status_data):
    #     model = CommonDb('user')
    #     consequence = model.selectAll(f"username='{status_data['username']}' and password='{status_data['password']}'")
    #     if consequence:
    #         result = False
    #         print('已有此用户，无法添加')
    #     else:
    #         result = model.add(status_data)
    #     return result

    def adduser_student_ServerStatus(self, status_data):
        model = CommonDb('student')
        consequence = model.selectAll(f"name='{status_data['username']}' and password='{status_data['password']}' and stu_no='{status_data['stu_no']}' and major='{status_data['major']}'")
        if consequence:
            result = False
            print('已有此用户，无法添加')
        else:
            result = model.add(status_data)
        return result

    def adduser_teacher_ServerStatus(self, status_data):
        model = CommonDb('teacher')
        consequence = model.selectAll(f"name='{status_data['username']}' and password='{status_data['password']}' and teach_no='{status_data['teach_no']}' and major='{status_data['major']}'")
        if consequence:
            result = False
            print('已有此用户，无法添加')
        else:
            result = model.add(status_data)
        return result

    def findlogin_student_ServerStatus(self, status_data):
        model = CommonDb('student')
        consequence = model.selectAll(f"username='{status_data['username']}' and password='{status_data['password']}'")
        if not consequence:
            result = False
            print('无此项')
        else:
            result = True
        return result

    def findlogin_teacher_ServerStatus(self, status_data):
        model = CommonDb('teacher')
        consequence = model.selectAll(f"username='{status_data['username']}' and password='{status_data['password']}'")
        if not consequence:
            result = False
            print('无此项')
        else:
            result = True
        return result

    def make_selfplan(self, status_data):
        model = CommonDb('student')
        consequence = model.selectAll(f"username='{status_data['username']}'")
        if not consequence:
            result = False
            print('无此项')
        else:
            result = True
        return {'result': result, 'consequence': consequence}

    def get_teacher_info_ServerStatus(self, status_data):
        model = CommonDb('teacher')
        consequence = model.selectAll(f"username='{status_data['username']}'")
        if not consequence:
            result = False
            print('无此项')
        else:
            result = True
        return {'result': result, 'consequence': consequence}

    def get_course_info_ServerStatus(self, status_data):
        model = CommonDb('course')
        consequence = model.selectAll(f"major='{status_data}'")
        print(consequence)
        if not consequence:
            result = False
            print('无此项')
        else:
            result = True
        return {'result': result, 'consequence': consequence}

    def delete_course_info_ServerStatus(self, status_data):
        model = CommonDb('course')
        major = status_data['major']



        info = "c" + str(status_data['course'])
        print(info)

        consequence = model.update_delete(info,f"major='{major}'")
        print(consequence)
        if not consequence:
            result = False
            print('无此项')
        else:
            result = True
        return {'result': result, 'consequence': consequence}