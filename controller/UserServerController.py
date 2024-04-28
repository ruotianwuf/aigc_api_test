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
        if status_data == '计算机科学':
            model = CommonDb('cs_course')


        elif status_data == '软件工程':
            model = CommonDb('se_course')

        consequence = model.selectAll_Direct(f"","course")

        if not consequence:
            result = False
            print('无此项')
        else:
            result = True
        return {'result': result, 'consequence': consequence}

    def output_string(self,elements):
        return '"' + ''.join(elements) + '"'

    # 调用函数

    def delete_course_info_ServerStatus(self, status_data):
        if status_data['major'] == '计算机科学':
            model = CommonDb('cs_course')

        elif status_data['major'] == '软件工程':
            model = CommonDb('se_course')

        course = status_data['course']

        print(self.output_string(course))
        course = str(self.output_string(course))
        consequence = model.delete_where(f"course={course}")
        print(consequence)
        if not consequence:
            result = False
            print('无此项')
        else:
            result = True
        return {'result': result, 'consequence': consequence}

    def add_course_info_ServerStatus(self, status_data):
        if status_data['major'] == '计算机科学':
            model = CommonDb('cs_course')
        elif status_data['major'] == '软件工程':
            model = CommonDb('se_course')
        course = status_data['course']
        consequence = model.selectAll(f"course='{course}'")
        if consequence:
            result = False
            print('已有此用户，无法添加')
        else:
            result = model.add({'course': course})
        return result
