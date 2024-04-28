import json
import os
import random
from flask import Flask, request, jsonify, render_template

from api_project_get.get_api import sync_vivogpt
from api_project_get.get_api_msg import sync_vivogpt_msg
from controller.UserServerController import UserServerController
from msg_api_test.msg_api_test import get_msg_answer

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
        result=sync_vivogpt_msg(data)
        print(result)
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

@app.route('/teacher', methods=['GET'])
def getteacher():
    return render_template('teacher.html')
@app.route('/teacher/home', methods=['GET'])
def getteacher_home():
    return render_template('teacher_home.html')


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
    info =get_info[0]
    major = info[4]
    major_course = con.get_course_info_ServerStatus(major)
    get_course_info = major_course['consequence']
    course_info = get_course_info[0]
    print(info)
    print(course_info)
    if result:
        return jsonify({'success': True, 'info': info, 'course_info': course_info}), 200
    else:
        return jsonify({'success': False}), 200


if __name__ == '__main__':
    app.run(debug=True)
