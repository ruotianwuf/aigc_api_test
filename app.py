import json
import os

from flask import Flask, request, jsonify, render_template

from api_project_get.get_api import sync_vivogpt
from api_project_get.get_api_msg import sync_vivogpt_msg
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
    return render_template('')

@app.route('/login', methods=['GET'])
def getlogin():
    return render_template('/')

@app.route('/login/student', methods=['GET'])
def getlogin_student():
    return render_template('login_student.html')

@app.route('/login/teacher', methods=['GET'])
def getlogin_teacher():
    return render_template('login_teacher.html')

if __name__ == '__main__':
    app.run(debug=True)
