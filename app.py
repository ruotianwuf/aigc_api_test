import io
import json
import os
import random
import datetime
import re
import pyautogui

from flask import Flask, request, jsonify, render_template, Response
from flask import jsonify,send_file
import requests

from PIL import Image
import base64

from api_project_get.get_email_api import send_email
from travel_attraction.get_TTS_attraction import get_tts_instance
from travel_attraction.get_api_travelAdvicei import sync_vivogpt_travelAdvice
from hw_pp_correct.correct import get_correct_check
from api_project_get.get_api import sync_vivogpt
from api_project_get.get_api_msg import sync_vivogpt_msg
from controller.UserServerController import UserServerController
from self_study_plan_project.get_plan_program import get_plan
from long_video_transfer.run_bat import run_bat_file
from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room
from work_careeradvice.get_api_careeradvice import sync_vivogpt_careeradvice
from healthtable.get_api import sync_vivogpt_ht, sync_vivogpt_traveladvice ,sync_vivogpt_place
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from work_careeradvice.get_api_careeradvice import sync_vivogpt_careeradvice
from work_interview.get_interview_api import sync_vivogpt_interview_writting,sync_vivogpt_interview_writting_answers
from work_interview.get_TTS_api import get_tts_instance, AueType, pcm2wav, TTS
from work_interview.get_interview_chat import sync_vivogpt_interview_chat

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jjj'

socketio = SocketIO()
socketio.init_app(app)


# 处理根路径请求，返回欢迎页面
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/smartlearn/', methods=['GET'])
def samartlearn():
    return render_template('smartlearn.html')

@app.route('/smartlife/', methods=['GET'])
def samartlife():
    return render_template('smartlife.html')

@app.route('/smartlife/travel', methods=['GET'])
def samartlife_travel():
    return render_template('travel.html')

@app.route('/smartlife/chat', methods=['GET'])
def samartlife_chat():
    return render_template('chatbox.html')

@app.route('/smartlife/travel/photofind', methods=['GET'])
def samartlife_photofind():
    return render_template('travel_photofind.html')

@app.route('/smartlife/travel/plan', methods=['GET'])
def samartlife_travelplan():
    return render_template('travel_plan.html')

@app.route('/smartlife/travel/attraction', methods=['GET'])
def samartlife_travelattraction():
    return render_template('travel_attraction.html')
@app.route('/smartlife/health', methods=['GET'])
def samartlife_health():
    return render_template('health.html')


@app.route('/smartlife/health/healthtable', methods=['GET'])
def samartlife_healthtable():
    return render_template('healthy_table.html')

@app.route('/smartlife/health/healthtest', methods=['GET'])
def samartlife_healthtest():
    return render_template('healthy_test.html')




@app.route('/health_answer', methods=['POST'])
def gethealthanswer_msg():
        data = json.loads(request.get_data(as_text=True))
        name = data['name']
        data = data['data']
        # data['love_sports'] = text_translate_c_to_e(data['love_sports'])
        # data = json.dumps(data)
        print(data)
        # data_need = json.dumps(data)

        con = UserServerController()
        res = con.insert_info(name,data)
        if not data == 1:
            result = sync_vivogpt_ht(str(data))
        else:
            result = None

        if result is not None and res:
            return jsonify({'success': True, 'result': result}), 200
        else:
            return jsonify({'success': False}), 200

@app.route('/travel_answer', methods=['POST'])
def get_travel_answer_msg():
        data = json.loads(request.get_data(as_text=True))
        data = data['city']
        # data['love_sports'] = text_translate_c_to_e(data['love_sports'])
        # data = json.dumps(data)
        print(data)
        # data_need = json.dumps(data)
        result = sync_vivogpt_traveladvice(data)
        if result:
            return jsonify({'success': True, 'result': result}), 200
        else:
            return jsonify({'success': False}), 200

@app.route('/health_info_get', methods=['POST'])
def gethealth_info():
        data = json.loads(request.get_data(as_text=True))
        name = data['name']
        con = UserServerController()
        res = con.get_healthy_info(name)

        if res[0][0] is not None:
            res = json.loads(res[0][0])
            # res['love_sports'] = text_translate_e_to_c(res['love_sports'])
            res = res
        else:
            res = 1
        if res:
            return jsonify({'success': True, 'result': res}), 200
        else :
            return jsonify({'success': True}), 200

@app.route('/table_commit', methods=['POST'])
def gettable_commit():
        data = json.loads(request.get_data(as_text=True))
        name = data['name']
        tdata = data['data']
        con = UserServerController()
        res = con.get_table_commit(name, tdata)

        if res:
            return jsonify({'success': True, 'result': res}), 200
        else :
            return jsonify({'success': True}), 200

@app.route('/table_get', methods=['POST'])
def gettable_get():
        data = json.loads(request.get_data(as_text=True))
        name = data['name']
        con = UserServerController()
        res = con.get_table_get(name)
        print(type(res))

        if res[0][0] is not None:
            res = json.loads(res[0][0])
        else:
            res = 1
        if res:
            return jsonify({'success': True, 'result': res}), 200
        else:
            return jsonify({'success': True}), 200
# @app.route('/file/upload/', methods=['POST', 'GET'])
# def upload():
#     try:
#         # get 请求返回上传页面
#         if request.method == 'GET':
#             return render_template('get_file_test.html')
#         if request.method == 'POST':
#             f = request.files['file']
#             paths = os.path.join('E:\\Python\\project\\Vivo_AIGC\\aigc_api_test\\static\\file')
#             da = os.path.exists(paths)
#             if da:
#                 ...
#             else:
#                 os.makedirs(paths)
#             upload_path = os.path.join(paths, f.filename)
#             f.save(upload_path)
#             return "上传成功"
#     except Exception as e:
#         print(e)
#         return {'code': 0, 'msg': f'{e}'}


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

@app.route('/answer_msg/career_advice', methods=['POST'])
def getanswer_careeradvice_msg():
    data = json.loads(request.get_data(as_text=True))
    question = data['question']
    result = sync_vivogpt_careeradvice(question)
    if result != None:
        return jsonify({'success': True, 'result': result}), 200
    else:
        return jsonify({'success': False}), 200
@app.route('/answer_msg/interview', methods=['POST'])
def getanswer_interview_msg():
    data = json.loads(request.get_data(as_text=True))
    question = data['question']
    result = sync_vivogpt_interview_writting(question)
    print(question)
    if result is not None:
        return jsonify({'success': True, 'result': result}), 200
    else:
        return jsonify({'success': False}), 200
@app.route('/answer_msg/interview/answer', methods=['POST'])
def getanswer_interview_answer():
    data = request.json
    questions = data['questions']
    result = sync_vivogpt_interview_writting_answers(questions)
    if result is not None:
        return jsonify({'success': True, 'result': result}), 200
    else:
        return jsonify({'success': False}), 200


@app.route('/answer_msg/interview/TTS', methods=['POST'])
def text_to_speech():
    data = request.json
    text = data.get('text', '你好')
    voice_type = data.get('voice_type', 'vivoHelper')
    engine_id = data.get('engine_id', 'short_audio_synthesis_jovi')

    tts = get_tts_instance(engine_id)
    tts.open()
    pcm_buffer = tts.gen_radio(aue=AueType.PCM, vcn=voice_type, text=text)
    if pcm_buffer:
        wav_io = pcm2wav(pcm_buffer)
        return send_file(
            wav_io,
            mimetype='audio/wav',
            as_attachment=True,
            download_name='output.wav'
        )
    else:
        return jsonify({'error': 'TTS generation failed'}), 500

@app.route('/answer_msg/interview/chat', methods=['POST'])
def getanswer_interview_chat():
    data = request.json
    questions = data['questions']
    result = sync_vivogpt_interview_chat(questions)
    if result:
        return jsonify({'success': True, 'recommend': result}), 200
    else:
        return jsonify({'success': True}), 200

@app.route('/answer', methods=['POST'])
def getanswer():
    data = json.loads(request.get_data(as_text=True))
    data = data['question']
    result = sync_vivogpt(data)
    if result != None:
        return jsonify({'success': True, 'result': result}), 200
    else:
        return jsonify({'success': False}), 200

@app.route('/smartlearn/student', methods=['GET'])
def getstudent():
    return render_template('student.html')


online_user = []
room_user = {}

@app.route('/smartlearn/student/advice', methods=['GET'])
def getstudent_advice():
    return render_template('student_advice.html')

@app.route('/smartlearn/student/course', methods=['GET'])
def getstudent_course():
    return render_template('student_course.html')

@app.route('/student/course/recommend', methods=['POST'])
def course_recommend_get():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    con = UserServerController()
    result = con.get_course_recommend()
    print(result)

    if result:
        return jsonify({'success': True, 'recommend': result}), 200
    else:
        return jsonify({'success': True}), 200


@app.route('/student/course/recommend/getiframe', methods=['POST'])
def course_recommend_getiframe():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    con = UserServerController()
    result = con.get_course_recommend_iframe(data)
    print(result)

    if result:
        return jsonify({'success': True, 'recommend': result}), 200
    else:
        return jsonify({'success': True}), 200



@app.route('/student/course/get', methods=['POST'])
def getstudent_course_get():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    con = UserServerController()
    result = con.get_student_info_ServerStatus(data)
    get_info = result['consequence']
    print(get_info)
    info = get_info[0]
    course_grade = []
    p = 0
    for i in get_info:
        content = i
        print(content,type(content))
        course_past = content[6]
        grade = content[7]
        # print(grade)
        if grade == None or grade == '':
            grade = '正在学习'
        # c_g = {'course': course_past, 'grade': grade}
        c_g = [course_past,grade]
        # print(type(c_g))
        course_grade.append(c_g)
    # print(course_grade)
    if result:
        return jsonify({'success': True, 'info': info, 'course_grade': course_grade, 'all_grade': info[4]}), 200
    else:
        return jsonify({'success': True}), 200


@app.route('/smartlearn/student/forum', methods=['GET'])
def getstudent_forum():
    return render_template('student_forum.html')

@app.route('/smartlearn/student/homework', methods=['GET'])
def getstudent_homework():
    return render_template('student_homework.html')

@app.route('/student/forum/post', methods=['POST'])
def getstudent_forum_submit_post():
    data = json.loads(request.get_data(as_text=True))
    sname = "'"+str(data['sname'])+"'"
    con = UserServerController()
    sid = con.get_sid(sname)
    print("sid"+str(sid))
    sid = ((list(sid))[0])[0]
    data['stu_no'] = sid
    data['date'] = datetime.datetime.today()
    data['post_no'] = 'p'+str(random.randint(1000000, 10000000))
    del data['sname']
    # print(data)
    result = con.add_post_ServerStatus(data)
    # print(result)
    if result:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 200

@app.route('/student/forum/comment', methods=['POST'])
def getstudent_forum_submit_comment():
    data = json.loads(request.get_data(as_text=True))
    data['date'] = datetime.datetime.today()
    data['com_no'] = 'c'+str(random.randint(100000, 1000000))
    print(data)
    con = UserServerController()
    result = con.add_comments_to_post_ServerStatus(data)

    print(result)
    if result:
        return jsonify({'success': True,}), 200
    else:
        return jsonify({'success': False}), 200

@app.route('/student/forum/like', methods=['POST'])
def getstudent_forum_like():
    data = json.loads(request.get_data(as_text=True))
    print(data)

    con = UserServerController()
    result = con.add_likes_to_post_ServerStatus(data)

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


@app.route('/smartlearn/teacher/live', methods=['GET'])
def get_teacher_live():
    return render_template('teacher_live.html')

@app.route('/smartlearn/student/live', methods=['GET'])
def get_student_live():
    return render_template('student_live.html')

@app.route('/pointer')
def pointer():
    x = int(float(request.args["xrate"]) * 1920)
    y = int(float(request.args["yrate"]) * 1080)
    # 执行点击操作
    pyautogui.click(x, y)
    return "success"



def gen():
    while True:
        screenShotImg = pyautogui.screenshot()

        imgByteArr = io.BytesIO()
        screenShotImg.save(imgByteArr, format='JPEG')
        imgByteArr = imgByteArr.getvalue()
        frame = imgByteArr
        yield (b'--frame\r\n Content-Type: image/jpeg\r\n\r\n' + frame)


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')




@app.route('/smartlearn/student/recommend', methods=['GET'])
def getstudent_recommend():
    return render_template('student_course_recommend.html')

@app.route('/smartlearn/student/recommend/video', methods=['GET'])
def get_Recommend_Video():
    return render_template('student_recommend_video.html')

@app.route('/smartlearn/teacher', methods=['GET'])
def getteacher():
    return render_template('teacher.html')
@app.route('/smartlearn/teacher/report', methods=['GET'])
def getteacher_report():
    return render_template('teacher_report.html')

@app.route('/smartlearn/teacher/upload', methods=['GET'])
def getteacher_upload():
    return render_template('teacher_upload.html')

@app.route('/smartlearn/teacher/check', methods=['GET'])
def getteacher_check():
    return render_template('teacher_check.html')

@app.route('/smartlearn/teacher/public', methods=['GET'])
def getteacher_public():
    return render_template('teacher_public.html')

@app.route('/smartlife/work', methods=['GET'])
def getwork():
    return render_template('work.html')
@app.route('/smartlife/work/career_advice', methods=['GET'])
def getcareer_advice():
    return render_template('career_advice.html')

@app.route('/smartlife/work/interview', methods=['GET'])
def getinterview():
    return render_template('interview.html')

@app.route('/smartlife/work/interview_question',methods=['GET'])
def getinterview_question():
    return render_template('interview_question.html')

@app.route('/test',methods=['GET'])
def gettest():
    return render_template('A-test.html')


@app.route('/teacher/public/get_sinfo', methods=['POST'])
def get_teacher_sinfo():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    con = UserServerController()
    result = con.get_teacher_info_ServerStatus(data)
    get_info = result['consequence']
    print(get_info)
    info =get_info[0]
    major = info[4]
    print(major)
    major_course = con.get_student_info(major)
    if major_course:
        return jsonify({'success': True, 'info': major_course}), 200
    else:
        return jsonify({'success': True}), 200

@app.route('/teacher/public/addgrade', methods=['POST'])
def add_course_grade():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    con = UserServerController()
    result = con.addcourse_grade(data)

    if result:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': True}), 200




@app.route('/smartlearn/adduser', methods=['GET'])
def adduser():
    return render_template('/')

@app.route('/smartlearn/adduser/student', methods=['GET'])
def adduser_student():
    return render_template('register_student.html')

@app.route('/smartlearn/adduser/teacher', methods=['GET'])
def adduser_teacher():
    return render_template('register_teacher.html')

@app.route('/smartlife/adduser/user', methods=['GET'])
def adduser_user():
    return render_template('register_user.html')


@app.route('/adduser/student/1', methods=['POST'])
def adduser_student_info():
    data = json.loads(request.get_data(as_text=True))
    data["stu_no"] = "s" + str(random.randint(100000000 - 1, 1000000000 - 1))
    print(data)
    con = UserServerController()
    result = con.adduser_student_ServerStatus(data)
    print(result)
    if result:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 200

@app.route('/adduser/teacher/1', methods=['POST'])
def adduser_teacher_info():
    data = json.loads(request.get_data(as_text=True))
    data["teach_no"] = "t" + str(random.randint(10000000 - 1, 100000000 - 1))
    print(data)
    con = UserServerController()
    result = con.adduser_teacher_ServerStatus(data)
    print(result)
    if result:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 200

@app.route('/get_email_code', methods=['POST'])
def get_email_code():
    data = json.loads(request.get_data(as_text=True))
    code = send_email(data['email'])
    if code:
        return jsonify({'success': True, 'code': code}), 200
    else:
        return jsonify({'success': False}), 200



@app.route('/adduser/user/1', methods=['POST'])
def adduser_user_info():
    if 'screenshot' not in request.files:
        return jsonify(success=False, message="没有文件部分")

    file = request.files['screenshot']
    print(file.mode)
    # 如果用户没有选择文件，浏览器也会提交一个没有文件名的空部分
    if file.filename == '':
        return jsonify(success=False, message="没有选择文件")

    filename = 'test2.png'
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    phone = request.form.get('phone')

    data = {'username': username, 'password': password, 'phone': phone, 'email': email}
    data["userid"] = "u" + str(random.randint(100000 - 1, 1000000 - 1))
    con = UserServerController()
    result = con.adduser_user_ServerStatus(data)

    image_path1 = 'static/humanphoto/test2.png'
    # base64_image1 = image_to_base64(image_path1)
    base64_image1 = image_to_base64(image_path1)
    img = {'blob': base64_image1}

    res = con.insert_blob_ServerStatus(username, img)
    print(res)

    print(data)


    if result and res:
        return jsonify({'success': True, 'data': result}), 200
    else:
        return jsonify({'success': False}), 200



@app.route('/smartlearn/login', methods=['GET'])
def getlogin():
    return render_template('/')



@app.route('/smartlearn/login/student', methods=['GET'])
def getlogin_student():
    return render_template('login_student.html')

@app.route('/smartlearn/login/teacher', methods=['GET'])
def getlogin_teacher():
    return render_template('login_teacher.html')

@app.route('/smartlife/login/user', methods=['GET'])
def getlogin_user():
    return render_template('login_user.html')

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





def image_to_base64(image_path):
    # 打开图片文件
    with Image.open(image_path) as img:
        # 创建一个字节流对象
        img_byte_arr = io.BytesIO()
        # 将图片保存到字节流中，这里使用PNG格式以保留透明度
        if img.mode == 'RGBA':
            img = img.convert('RGBA')  # 确保图像是RGBA模式
            img.save(img_byte_arr, format='PNG')
        else:
            img.save(img_byte_arr, format='PNG')

        # 重置字节流对象的位置指针到开始位置
        img_byte_arr.seek(0)

        # 获取字节流中的二进制数据
        img_byte_arr = img_byte_arr.getvalue()

        # 使用base64库将二进制数据编码为Base64格式
        base64_image = base64.b64encode(img_byte_arr).decode('utf-8')

    return base64_image


UPLOAD_FOLDER = 'static/humanphoto'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/login/user/1', methods=['POST'])
def getlogin_user_info():
    if 'screenshot' not in request.files:
        return jsonify(success=False, message="没有文件部分")

    file = request.files['screenshot']
    print(file.mode)
    # 如果用户没有选择文件，浏览器也会提交一个没有文件名的空部分
    if file.filename == '':
        return jsonify(success=False, message="没有选择文件")


    filename = 'test.png'
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    username = request.form.get('username')
    password = request.form.get('password')
    phone = request.form.get('phone')

    data = {'username': username, 'password': password, 'phone': phone}

    # print(base64_image2)
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"

    # image_path1 = 'static/humanphoto/'+str(username)+str(phone)+'.png'
    # base64_image1 = image_to_base64(image_path1)

    con = UserServerController()
    base64_image1 = con.find_blob_ServerStatus(data)
    base64_image1 = json.loads(base64_image1[0][0])
    base64_image1 = base64_image1['blob']
    # base64_image1 = base64_image1.decode('utf-8')
    print(base64_image1)

    image_path2 = 'static/humanphoto/test.png'
    base64_image2 = image_to_base64(image_path2)



    params_str = [
                    {
                        "image": base64_image1,
                        "image_type": "BASE64",
                        "face_type": "LIVE",
                        "quality_control": "LOW"
                    },
                    {
                        "image": base64_image2,
                        "image_type": "BASE64",
                        "face_type": "LIVE",
                        "quality_control": "LOW"
                    }
                ]
    print(type(params_str))

    # params_str = json.dumps(params_str, ensure_ascii=True)
    # print(type(params_str))

    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=n6MEdq40kQfFINA5J0cC4rLu&client_secret=Hz91ksY1oVVob4MAis9QycbfXR1IfKzJ'
    response = requests.get(host)
    if response:
        print(type(response.json()))
    at = response.json()
    access_token = at['access_token']
    request_url = request_url + "?access_token=" + access_token
    print(request_url)
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, json=params_str, headers=headers)
    if response:
        result = response.json()
        print(result['result']['score'])
        num = int(result['result']['score'])


    print(data)

    result = con.findlogin_user_ServerStatus(data)
    if result and num >= 80:
        return jsonify({'success': True, 'data': result}), 200
    else:
        return jsonify({'success': False}), 200


@app.route('/smartlearn/teacher/info', methods=['GET'])
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
@app.route('/smartlearn/teacher/upload_homework', methods=['GET', 'POST'])
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
            elif file_type == 'hw_answer':
                upload_dir = os.path.join(app.root_path, 'static', 'file', 'hw_answer')
            elif file_type == 'courseware':
                upload_dir = os.path.join(app.root_path, 'static', 'file', 'courseware')
            elif file_type == 'paper':
                upload_dir = os.path.join(app.root_path, 'static', 'file', 'paper')
            elif file_type == 'pp_answer':
                upload_dir = os.path.join(app.root_path, 'static', 'file', 'pp_answer')
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
@app.route('/teacher/delete_file/homework', methods=['DELETE'])
def delete_file_homework():
    file_name = request.args.get('fileName')
    file_path = os.path.join(app.root_path, 'static', 'file','homework',file_name)
    try:
        os.remove(file_path)
        return jsonify({'success': True, 'message': '文件删除成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/teacher/delete_file/hw_answer', methods=['DELETE'])
def delete_file_hw_answer():
    file_name = request.args.get('fileName')
    file_path = os.path.join(app.root_path, 'static', 'file','hw_answer',file_name)
    try:
        os.remove(file_path)
        return jsonify({'success': True, 'message': '文件删除成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/teacher/delete_file/courseware', methods=['DELETE'])
def delete_file_courseware():
    file_name = request.args.get('fileName')
    file_path = os.path.join(app.root_path, 'static', 'file','courseware',file_name)
    try:
        os.remove(file_path)
        return jsonify({'success': True, 'message': '文件删除成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/teacher/delete_file/paper', methods=['DELETE'])
def delete_file_paper():
    file_name = request.args.get('fileName')
    file_path = os.path.join(app.root_path, 'static', 'file','paper',file_name)
    try:
        os.remove(file_path)
        return jsonify({'success': True, 'message': '文件删除成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/teacher/delete_file/pp_answer', methods=['DELETE'])
def delete_file_pp_answer():
    file_name = request.args.get('fileName')
    file_path = os.path.join(app.root_path, 'static', 'file','pp_answer',file_name)
    try:
        os.remove(file_path)
        return jsonify({'success': True, 'message': '文件删除成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/teacher/file_list/homework', methods=['GET'])
def get_file_list_homework():
    upload_dir = 'static/file/homework'
    file_list = os.listdir(upload_dir)
    return jsonify(file_list)

@app.route('/teacher/file_list/hw_answer', methods=['GET'])
def get_file_list_hw_answer():
    upload_dir = 'static/file/hw_answer'
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


@app.route('/teacher/file_list/pp_answer', methods=['GET'])
def get_file_list_pp_answer():
    upload_dir = 'static/file/pp_answer'
    file_list = os.listdir(upload_dir)
    return jsonify(file_list)



@app.route('/teacher/upload_video', methods=['POST'])
def upload_video():
    video_file = request.files['video']
    upload_dir = os.path.join(app.root_path, 'long_video_transfer')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    new_filename = 'test.wav'
    video_file.save(os.path.join(upload_dir, new_filename))
    run_bat_file()
    file_path = 'long_video_transfer/aigc_content.txt'
        # 使用with语句打开文件，确保在使用完文件后正确关闭
    with open(file_path, 'r', encoding='utf-8') as file:
            # 使用read()方法读取文件内容
        print("正在读取")
        file_content = file.read()
        print(file_content)
    response_data = {'success': True, 'message': 'Video uploaded successfully','content': file_content}
    # os.remove(video_file.filename)
    return jsonify(response_data), 200

@app.route('/student/upload_homework', methods=['POST'])
def upload_student_homework():
    homework_file = request.files['homework']
    upload_dir = os.path.join(app.root_path, 'static/student_upload/homework')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    homework_file.save(os.path.join(upload_dir, homework_file.filename))
    print("上传完成")
    check_result = get_correct_check(upload_dir+'/'+homework_file.filename)
    response_data = {'success': True, 'message': 'Homework uploaded successfully', 'check': check_result}
    return jsonify(response_data), 200


@app.route('/insertmsg', methods=['POST'])
def get_insert_live_msg():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    con = UserServerController()
    result = con.insert_live_info(data)
    if result:
        return jsonify({'success': True}), 200

@app.route('/getmsg', methods=['POST'])
def get_get_live_msg():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    con = UserServerController()
    result = con.get_live_info(data)
    if result:
        return jsonify({'success': True, 'result': result}), 200

@app.route('/getchatmsg', methods=['POST'])
def get_get_chat_msg():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    con = UserServerController()
    result = con.get_chatmsg_info(data)
    if result:
        return jsonify({'success': True, 'data': result}), 200

@app.route('/getchatmanmsg', methods=['POST'])
def get_get_chatman_msg():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    con = UserServerController()
    result = con.get_chatmanmsg_info(data)
    if result:
        return jsonify({'success': True, 'data': result}), 200


@app.route('/insertchatmsg', methods=['POST'])
def get_insert_chat_msg():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    con = UserServerController()
    result = con.insert_chatmsg_info(data)
    if result:
        return jsonify({'success': True}), 200

@app.route('/deletechatbox', methods=['POST'])
def delete_chat_man():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    con = UserServerController()
    result = con.delete_chatman(data)
    if result:
        return jsonify({'success': True}), 200

@app.route('/addchatbox', methods=['POST'])
def add_chat_man():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    con = UserServerController()
    result = con.add_chatman(data)
    if result:
        return jsonify({'success': True}), 200


UPLOAD= 'static/location'
app.config['UPLOAD'] = UPLOAD
def get_access_token():
    API_KEY = 'krDViPrnNz62q5XFueECkfCN'
    SECRET_KEY = 'LfSpJRSp34S6IpEnwsmhduz99cglCxnI'
    token_url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}'
    response = requests.get(token_url)
    return response.json().get('access_token')


@app.route('/get_address', methods=['POST'])
def get_address():
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')

    # 反向地理编码获取详细地址，设置语言为中文
    url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lng}&key=79b89ebd09984761a4797e0c61009fc9&language=zh"
    response = requests.get(url)
    if response.status_code == 200:
        address = response.json()['results'][0]['formatted']
    else:
        address = '未知地址'

    return jsonify({"status": "success", "address": address})


@app.route('/get_nearby_places', methods=['POST'])
def get_nearby_places():
    data = request.json
    address = data.get('address')

    question = f"这是我现在所处的位置：{address}，列出该地址附近5km内的五个景点或者更少，选择的景点按照名气等级排序，并详细讲解介绍每个景点的距离当前位置的距离，历史背景，游玩攻略等详细信息，每个景点的讲解不少于200字。"
    advice = sync_vivogpt_travelAdvice(question)

    return jsonify({"status": "success", "advice": advice})


# 地表识别的路由
@app.route('/smartlife/travel/recognize-landmark', methods=['POST'])
def recognize_landmark():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No selected image'}), 400

    # 使用统一的文件名
    unique_filename = 'photofind.jpg'
    image_path = os.path.join(app.config['UPLOAD'], unique_filename)
    image_file.save(image_path)

    # 调用百度地表识别API
    access_token = get_access_token()
    api_url = f'https://aip.baidubce.com/rest/2.0/image-classify/v1/landmark?access_token={access_token}'

    # 将图片转换为base64编码
    with open(image_path, 'rb') as f:
        img = base64.b64encode(f.read())

    params = {"image": img}
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(api_url, data=params, headers=headers)

    # 处理API响应
    if response.ok:
        result = response.json()
        print(result)
        print(result['result']['landmark'])
        res = sync_vivogpt_place(str(result['result']['landmark']))
        # 返回识别结果
        return jsonify({'success': True, 'nameRes': result['result']['landmark'], 'details': res}), 200
    else:
        # 返回错误信息
        return jsonify({'error': 'Failed to recognize landmark'}), response.status_code


if __name__ == '__main__':
   app.run(debug=False,  port=2750)
#

