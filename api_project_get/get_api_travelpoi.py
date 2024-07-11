import requests
import hashlib
import hmac
import time

from .auth_util import gen_sign_headers


# 请注意替换APP_ID、APP_KEY
APP_ID = '3032660331'
APP_KEY = 'LxpYKtKbgakYmMTN'
DOMAIN = 'api-ai.vivo.com.cn'
URI = '/search/geo'
METHOD = 'GET'


def get_poi(lat, lon, keywords='景点', page_num=1, page_size=1):
    """ 获取附近景点信息 """
    params = {
        'keywords': keywords,
        'location': f"{lat},{lon}",
        'page_num': page_num,
        'page_size': page_size
    }

    headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)
    url = f'http://{DOMAIN}{URI}'
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()['pois'][0]
    else:
        return {'error': response.text}


def get_explanation(poi_name):
    """ 获取景点讲解 """
    params = {
        'query': poi_name
    }
    headers = gen_sign_headers(APP_ID, APP_KEY, 'POST', URI, params)
    url = f'http://{DOMAIN}{URI}'
    response = requests.post(url, data=params, headers=headers)

    if response.status_code == 200:
        return response.json()['answer']
    else:
        return {'error': response.text}