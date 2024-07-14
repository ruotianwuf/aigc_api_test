# encoding: utf-8
import uuid
import time
import requests
from work_interview.auth_util import gen_sign_headers

message = []


def sync_vivogpt_interview_chat(ask):
    APP_ID = '3032660331'
    APP_KEY = 'LxpYKtKbgakYmMTN'
    URI = '/vivogpt/completions'
    DOMAIN = 'api-ai.vivo.com.cn'

    message.append({"content": ask, "role": "user"})
    print(message)
    METHOD = 'POST'

    params = {
        'requestId': str(uuid.uuid4())
    }
    print('requestId:', params['requestId'])

    data = {
        'messages': message,
        'model': 'vivo-BlueLM-TB',
        'sessionId': str(uuid.uuid4()),
        'extra': {
            'temperature': 0.9
        },
        'systemPrompt': '你的名字是蓝心ai面试官，你需要根据面试者希望面试的岗位，提出一些面试中常见的问题，不用过多关注专业方面的内容'
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
            message.append({"content": content, "role": "assistant"})
            print(message)
            return content
    else:
        print(response.status_code, response.text)

    end_time = time.time()
    timecost = end_time - start_time
    print('请求耗时: %.2f秒' % timecost)

# if __name__ == '__main__':
#     sync_vivogpt_interview_chat('你好')