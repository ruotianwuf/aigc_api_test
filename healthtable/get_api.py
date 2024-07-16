# encoding: utf-8
import uuid
import time
import requests
from healthtable.auth_util import gen_sign_headers

def sync_vivogpt_ht(prompt):

    APP_ID = '3032660331'
    APP_KEY = 'LxpYKtKbgakYmMTN'
    URI = '/vivogpt/completions'
    DOMAIN = 'api-ai.vivo.com.cn'

    # prompt = str({'体重': '80kg', '身高': '170cm', '爱好': '骑行', '期望体重': '60kg'})
    print(prompt)
    METHOD = 'POST'

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
        'systemPrompt': '你的中文名字叫健康日程安排助手，当回复问题时需要回复你的名字时，中文名必须回复健康日程安排助手，此外回复和你的名字相关的问题时，也需要给出和你的名字对应的合理回复。需要你通过内容来分析安排健康日程，周一到周日七天，每天的早中晚三餐，每天锻炼的时间和内容，时间精确到具体时间段,以日程表的形式输出'
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


def sync_vivogpt_traveladvice(prompt):

    APP_ID = '3032660331'
    APP_KEY = 'LxpYKtKbgakYmMTN'
    URI = '/vivogpt/completions'
    DOMAIN = 'api-ai.vivo.com.cn'

    # prompt = str({'体重': '80kg', '身高': '170cm', '爱好': '骑行', '期望体重': '60kg'})
    print(prompt)
    METHOD = 'POST'

    params = {
        'requestId': str(uuid.uuid4())
    }
    print('requestId:', params['requestId'])

    data = {
        'prompt': str(prompt),

        'model': 'vivo-BlueLM-TB',
        'sessionId': str(uuid.uuid4()),
        'extra': {
            'temperature': 0.9
        },
        'systemPrompt': '你的中文名字叫旅行攻略和计划安排助手，当回复问题时需要回复你的名字时，中文名必须回复旅行攻略和计划安排助手，此外回复和你的名字相关的问题时，也需要给出和你的名字对应的合理回复。需要你通过输入的城市来生成一个旅游攻略，包括景点，美食，路线，推荐旅游时间，并给出对应国家的其他城市推荐'
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

# sync_vivogpt_traveladvice("成都")