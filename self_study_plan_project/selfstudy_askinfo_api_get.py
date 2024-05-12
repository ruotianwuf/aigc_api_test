# encoding: utf-8
import uuid
import time
import requests
from api_project_get.auth_util import gen_sign_headers

def sync_vivogpt_selfplan(prompt):

    APP_ID = '3032660331'
    APP_KEY = 'LxpYKtKbgakYmMTN'
    URI = '/vivogpt/completions'
    DOMAIN = 'api-ai.vivo.com.cn'


    METHOD = 'POST'

    prompt = '根据学生信息生成详细未来学习计划并推荐对应专业的课程,必须有具体的执行任务和未来要上的课程等，grade是已学内容的综合成绩，course_past是已经选择的课程，c_grade是对应course_past这一门课的成绩评级，如果没有成绩或成绩未知则说明这门课是当前学生正在上的课；不要生成字典回答，请处理成成段回答' + str(prompt)

    params = {
        'requestId': str(uuid.uuid4())
    }
    print('requestId:', params['requestId'])

    data = {
        'prompt': prompt,

        'model': 'vivo-BlueLM-TB',
        'sessionId': str(uuid.uuid4()),
        'extra': {
            'temperature': 0.9
        },
        'systemPrompt': '你的中文名字叫未来学习计划助手，当回复问题时需要回复你的名字时，中文名必须回复未来学习计划助手，此外回复和你的名字相关的问题时，也需要给出和你的名字对应的合理回复。当给你传输和学生课程和学习情况的时候，只生成对应且合理的学习计划。并且成绩是A+最好其余依次向下。如果成绩未知，则说明这门课是学生正在上的课程；内容必须准确有可行性、且内容必须详细'
    }
    headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)
    headers['Content-Type'] = 'application/json'

    start_time = time.time()
    url = 'https://{}{}'.format(DOMAIN, URI)
    response = requests.post(url, json=data, headers=headers, params=params)

    if response.status_code == 200:
        res_obj = response.json()
        print(f'response:{res_obj}')
        if res_obj['code'] == 0 and res_obj.get('data'):
            content = res_obj['data']['content']
            print(f'final content:\n{content}')
            return content

    else:
        print(response.status_code, response.text)


    end_time = time.time()
    timecost = end_time - start_time
    print('请求耗时: %.2f秒' % timecost)






