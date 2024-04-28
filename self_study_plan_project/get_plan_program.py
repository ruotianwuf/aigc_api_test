from controller.UserServerController import UserServerController
from self_study_plan_project.selfstudy_askinfo_api_get import sync_vivogpt_selfplan


def get_plan(info):
    con = UserServerController()
    condition = con.make_selfplan(info)
    print(condition)
    condition_list=condition['consequence']
    condition_list_info = condition_list[0]
    print(condition_list_info)
    name = condition_list_info[1]
    student_id = condition_list_info[3]
    grade = condition_list_info[4]
    major = condition_list_info[5]
    course_now = condition_list_info[6]
    course_past = condition_list_info[7]
    data = {'name': name, 'student_id': student_id, 'grade': grade, 'major': major,'course_now': course_now,'course_past': course_past}
    print(data)

    res = sync_vivogpt_selfplan(data)
    print(res)
    return res



get_plan({"username": '11'})