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
        consequence = model.selectAll(f"username='{status_data['username']}' and password='{status_data['password']}' and stu_no='{status_data['stu_no']}' and major='{status_data['major']}'")
        consequence2 = model.selectAll(f"username='{status_data['username']}'")
        # print("啊？" + str(consequence2))
        print(consequence)
        if consequence != None:
            flag1 = False
        else:
            flag1 = True
        if consequence2 != None:
            flag = False
        else:
            flag = True
        if flag1 and not flag:
            result = False
            print('已有此用户，无法添加')
        else:
            result = model.add(status_data)
        return result

    def adduser_teacher_ServerStatus(self, status_data):
        model = CommonDb('teacher')
        consequence = model.selectAll(f"username='{status_data['username']}' and password='{status_data['password']}' and teach_no='{status_data['teach_no']}' and major='{status_data['major']}'")
        consequence2 = model.selectAll(f"username='{status_data['username']}'")
        # print("啊？"+str(consequence2))
        print(consequence)
        if consequence != None:
            flag1 = False
        else:
            flag1 = True
        if consequence2 != None:
            flag = False
        else:
            flag = True
        if flag1 and not flag:
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

    def find_student_ServerStatus(self, status_data):
        model = CommonDb('student')
        consequence = model.selectAll(f"username='{status_data['username']}'")
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


    def get_student_info_ServerStatus(self, status_data):
        model = CommonDb('student')
        consequence = model.selectAll(f"username='{status_data['username']}'")
        if not consequence:
            result = False
            print('无此项')
        else:
            result = True
        return {'result': result, 'consequence': consequence}


    def get_course_info_ServerStatus(self, status_data):
        model = CommonDb('course')

        consequence = model.selectAll_Direct(f"major='{status_data}'","course")

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
        model = CommonDb('course')
        course = status_data['course']
        course ='"' + course[0] +'"'
        consequence = model.delete_where(f"course={course} and major='{status_data['major']}'")
        print(consequence)
        if not consequence:
            result = False
            print('无此项')
        else:
            result = True
        return {'result': result, 'consequence': consequence}

    def add_course_info_ServerStatus(self, status_data):
        # if status_data['major'] == '计算机科学':
        #     model = CommonDb('cs_course')
        # elif status_data['major'] == '软件工程':
        #     model = CommonDb('se_course')
        model = CommonDb('course')
        course = status_data['course']
        consequence = model.selectAll(f"course='{course}'")
        if consequence:
            result = False
            print('已有，无法添加')
        else:
            result = model.add({'course': course, 'major': status_data['major']})
        return result

    def find_student_Post_ServerStatus(self,data):
        if self.find_student_ServerStatus(data):
            post_model = CommonDb('post')
            comment_model = CommonDb('comment')
            post_consequence = post_model.selectAllPost_Direct(f"")
            comment_consequence = comment_model.selectAllPost_Direct(f"")
            print(post_consequence)
            print(comment_consequence)
            return {'Post': post_consequence, 'Comment': comment_consequence}

    def add_likes_to_post_ServerStatus(self,data):
        model = CommonDb('post')
        likes = {'like_count': int(data['like']) + 1}
        consequence = model.update(likes,'post_no='+str('"'+data['post_no']+'"'))
        print(consequence)
        return True

    def add_comments_to_post_ServerStatus(self,data):
        model = CommonDb('comment')

        consequence = model.add_comment(data)
        print(consequence)
        return True

    def add_post_ServerStatus(self,data):
        model = CommonDb('post')

        consequence = model.add_comment(data)
        print(consequence)
        return True

    def get_sid(self,sname):
        model = CommonDb('student')
        consequence = model.select_sid(sname)
        return consequence