from controller.UserServerController import UserServerController
from self_study_plan_project.selfstudy_askinfo_api_get import sync_vivogpt_selfplan


def get_plan(info):
    con = UserServerController()
    condition = con.make_selfplan(info)
    print(condition)
    condition_list=condition['consequence']
    print(len(condition_list))
    message = {}

    for i in range(len(condition_list)):
        condition_list_info = condition_list[i]
    # print(condition_list_info)
        name = condition_list_info[1]
        student_id = condition_list_info[2]
        grade = condition_list_info[4]
        major = condition_list_info[5]
        course_past = condition_list_info[6]
        c_grade = condition_list_info[7]
        if c_grade == '':
            c_grade = '正在学习'
        data = {'name': name, 'student_id': student_id, 'grade': grade, 'major': major,'course_past': course_past,'c_grade': c_grade}
        message[i] = data
    print(message)

    res = sync_vivogpt_selfplan(message)
    print(res)
    return res


#
# get_plan({"username": '11'})