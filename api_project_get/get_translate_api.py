import uuid
import requests
from api_project_get.auth_util import gen_sign_headers

# 注意替换APP_ID、APP_KEY
APP_ID = '3032660331'
APP_KEY = 'LxpYKtKbgakYmMTN'
URI = '/translation/query/self'
DOMAIN = 'api-ai.vivo.com.cn'
METHOD = 'POST'



def text_translate_e_to_c(text):
    data = {
        'from': 'en',
        'to': 'zh-CHS',
        'text': text,
        'app': 'test',
        'requestId': str(uuid.uuid4())
    }
    params = {}
    headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)
    # print('headers', headers)
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    url = 'https://{}{}'.format(DOMAIN, URI)

    res = requests.post(url=url, headers=headers, data=data)

    if res.status_code == 200:
        print(res.json())
        result = res.json()
        return result['data']['translation']

    else:
        print(res.status_code, res.text)
        return None


def text_translate_c_to_e(text):
    data = {
        'from': 'zh-CHS',
        'to': 'en',
        'text': text,
        'app': 'test',
        'requestId': str(uuid.uuid4())
    }
    params = {}
    headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)
    # print('headers', headers)
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    url = 'https://{}{}'.format(DOMAIN, URI)

    res = requests.post(url=url, headers=headers, data=data)

    if res.status_code == 200:
        print(res.json())
        result = res.json()
        return result['data']['translation']

    else:
        print(res.status_code, res.text)
        return None


