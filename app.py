import json
import os
import random
from flask import Flask, request, jsonify, render_template

from api_project_get.get_api import sync_vivogpt
from api_project_get.get_api_msg import sync_vivogpt_msg
from controller.UserServerController import UserServerController
from msg_api_test.msg_api_test import get_msg_answer
from self_study_plan_project.get_plan_program import get_plan

app = Flask(__name__)

# 处理根路径请求，返回欢迎页面
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/file/upload/', methods=['POST', 'GET'])
def upload():
    try:
        # get 请求返回上传页面
        if request.method == 'GET':
            return render_template('get_file_test.html')
        if request.method == 'POST':
            f = request.files['file']
            paths = os.path.join('E:\\Python\\project\\Vivo_AIGC\\aigc_api_test\\static\\file')
            da = os.path.exists(paths)
            if da:
                ...
            else:
                os.makedirs(paths)
            upload_path = os.path.join(paths, f.filename)
            f.save(upload_path)
            return "上传成功"
    except Exception as e:
        print(e)
        return {'code': 0, 'msg': f'{e}'}


@app.route('/answer_msg', methods=['POST'])
def getanswer_msg():
        data = json.loads(request.get_data(as_text=True))
        data = data['question']
        result = sync_vivogpt_msg(data)
        print(result)
        if result != None:
            return jsonify({'success': True, 'result': result}), 200
        else:
            return jsonify({'success': False}), 200

@app.route('/answer_msg/advice', methods=['POST'])
def getanswer_advice_msg():
        data = json.loads(request.get_data(as_text=True))
        result = get_plan(data)
        print('内容:'+result)
        if result != None:
            return jsonify({'success': True, 'result': result}), 200
        else:
            return jsonify({'success': False}), 200

@app.route('/answer', methods=['POST'])
def getanswer():
    data = json.loads(request.get_data(as_text=True))
    data = data['question']
    result = sync_vivogpt(data)
    if result != None:
        return jsonify({'success': True, 'result': result}), 200
    else:
        return jsonify({'success': False}), 200

@app.route('/student', methods=['GET'])
def getstudent():
    return render_template('student.html')

@app.route('/student/advice', methods=['GET'])
def getstudent_advice():
    return render_template('student_advice.html')

@app.route('/student/course', methods=['GET'])
def getstudent_course():
    return render_template('student_course.html')

@app.route('/student/forum', methods=['GET'])
def getstudent_forum():
    return render_template('student_forum.html')

@app.route('/student/forum/comment', methods=['POST'])
def getstudent_forum_submit_comment():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    # con = UserServerController()
    # result = con.find_student_Post_ServerStatus(data)
    result = True
    print(result)
    if result:
        return jsonify({'success': True,}), 200
    else:
        return jsonify({'success': False}), 200

@app.route('/student/forum/getPost', methods=['POST'])
def getstudent_forum_post():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    con = UserServerController()
    result = con.find_student_Post_ServerStatus(data)
    print(result)
    if result:
        return jsonify({'success': True, 'result': result}), 200
    else:
        return jsonify({'success': False}), 200

@app.route('/student/grades', methods=['GET'])
def getstudent_grades():
    return render_template('student_grades.html')

@app.route('/teacher', methods=['GET'])
def getteacher():
    return render_template('teacher.html')
@app.route('/teacher/home', methods=['GET'])
def getteacher_home():
    return render_template('teacher_home.html')

@app.route('/teacher/upload', methods=['GET'])
def getteacher_upload():
    return render_template('teacher_upload.html')

@app.route('/teacher/check', methods=['GET'])
def getteacher_check():
    return render_template('teacher_check.html')

@app.route('/teacher/public', methods=['GET'])
def getteacher_public():
    return render_template('teacher_public.html')

@app.route('/adduser', methods=['GET'])
def adduser():
    return render_template('/')

@app.route('/adduser/student', methods=['GET'])
def adduser_student():
    return render_template('')

@app.route('/adduser/teacher', methods=['GET'])
def adduser_teacher():
    return render_template('register_teacher.html')

@app.route('/adduser/student/1', methods=['POST'])
def adduser_student_info():
    data = json.loads(request.get_data(as_text=True))
    data["stu_no"] = "s" + str(random.randint(100000000 - 1, 1000000000 - 1))
    print(data)
    con = UserServerController()
    result = con.adduser_student_ServerStatus(data)
    print(result)
    return jsonify({'success': True}), 200

@app.route('/adduser/teacher/1', methods=['POST'])
def adduser_teacher_info():
    data = json.loads(request.get_data(as_text=True))
    data["teach_no"] = "t" + str(random.randint(10000000 - 1, 100000000 - 1))
    print(data)
    con = UserServerController()
    result = con.adduser_teacher_ServerStatus(data)
    print(result)
    return jsonify({'success': True}), 200



@app.route('/login', methods=['GET'])
def getlogin():
    return render_template('/')

@app.route('/login/student', methods=['GET'])
def getlogin_student():
    return render_template('login_student.html')

@app.route('/login/teacher', methods=['GET'])
def getlogin_teacher():
    return render_template('login_teacher.html')

@app.route('/login/teacher/1', methods=['POST'])
def getlogin_teacher_info():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    con = UserServerController()
    result = con.findlogin_teacher_ServerStatus(data)
    if result:
        return jsonify({'success': True, 'data': result}), 200
    else:
        return jsonify({'success': False}), 200

@app.route('/login/student/1', methods=['POST'])
def getlogin_student_info():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    con = UserServerController()
    result = con.findlogin_student_ServerStatus(data)
    if result:
        return jsonify({'success': True, 'data': result}), 200
    else:
        return jsonify({'success': False}), 200



@app.route('/teacher/info', methods=['GET'])
def teacher_info():
    return render_template('teacher_data_info.html')


@app.route('/teacher/info/get', methods=['POST'])
def get_teacher_info():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    con = UserServerController()
    result = con.get_teacher_info_ServerStatus(data)
    get_info = result['consequence']
    print(get_info)
    info =get_info[0]
    major = info[4]
    print(major)
    major_course = con.get_course_info_ServerStatus(major)
    get_course_info = major_course['consequence']

    print("course_info", get_course_info)


    if result:
        return jsonify({'success': True, 'info': info, 'course_info': get_course_info}), 200
    else:
        return jsonify({'success': True}), 200

@app.route('/teacher/info/c_delete', methods=['POST'])
def delete_teacher_c_info():

    data = json.loads(request.get_data(as_text=True))
    print(data)

    con = UserServerController()

    result = con.delete_course_info_ServerStatus(data)
    if result:
        return jsonify({'success': True}), 200

@app.route('/teacher/info/addcourse', methods=['POST'])
def add_teacher_c_info():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    con = UserServerController()
    result = con.add_course_info_ServerStatus(data)
    if result:
        return jsonify({'success': True}), 200


# 老师上传作业页面路由
@app.route('/teacher/upload_homework', methods=['GET', 'POST'])
def upload_homework():
    if request.method == 'GET':
        return render_template('teacher_upload_homework.html')
    elif request.method == 'POST':
        try:
            # 获取上传的文件
            uploaded_file = request.files['file']

            # 获取上传文件类型
            file_type = request.form['fileType']

            # 指定上传文件保存的路径
            if file_type == 'homework':
                upload_dir = os.path.join(app.root_path, 'static', 'file', 'homework')
            elif file_type == 'courseware':
                upload_dir = os.path.join(app.root_path, 'static', 'file', 'courseware')
            elif file_type == 'paper':
                upload_dir = os.path.join(app.root_path, 'static', 'file', 'paper')
            else:
                raise Exception('Invalid file type')

            # 如果目录不存在则创建
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            # 将文件保存到指定路径
            uploaded_file.save(os.path.join(upload_dir, uploaded_file.filename))

            return render_template('teacher_upload.html', upload_success=True)
        except Exception as e:
            return render_template('teacher_upload.html', upload_error=str(e))


# 处理删除文件的请求
@app.route('/teacher/delete_file', methods=['DELETE'])
def delete_file():
    file_name = request.args.get('fileName')
    file_path = os.path.join(app.root_path, 'static', 'file', file_name)
    try:
        os.remove(file_path)
        return jsonify({'success': True, 'message': '文件删除成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# # 用于返回文件列表
# @app.route('/teacher/file_list', methods=['GET'])
# def get_file_list():
#     upload_dir = 'static/file'
#     file_list = os.listdir(upload_dir)
#     return jsonify(file_list)

@app.route('/teacher/file_list/homework', methods=['GET'])
def get_file_list_homework():
    upload_dir = 'static/file/homework'
    file_list = os.listdir(upload_dir)
    return jsonify(file_list)

@app.route('/teacher/file_list/courseware', methods=['GET'])
def get_file_list_courseware():
    upload_dir = 'static/file/courseware'
    file_list = os.listdir(upload_dir)
    return jsonify(file_list)

@app.route('/teacher/file_list/paper', methods=['GET'])
def get_file_list_paper():
    upload_dir = 'static/file/paper'
    file_list = os.listdir(upload_dir)
    return jsonify(file_list)

if __name__ == '__main__':
    app.run(debug=True)
