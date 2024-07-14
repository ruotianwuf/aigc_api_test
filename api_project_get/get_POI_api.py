#!/usr/bin/env python
# encoding: utf-8

import requests
from work_careeradvice.auth_util import gen_sign_headers

# 请注意替换APP_ID、APP_KEY
APP_ID = '3032660331'
APP_KEY = 'LxpYKtKbgakYmMTN'
DOMAIN = 'api-ai.vivo.com.cn'
URI = '/search/geo'
METHOD = 'GET'


def geocode_poi():
    """ 地理编码（poi搜索） """
    params = {
        'keywords': '春熙路',
        'city': '成都',
        'page_num': 1,
        'page_size': 3
    }
    headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)
    print('headers:', headers)
    url = 'http://{}{}'.format(DOMAIN, URI)
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
    else:
        data = response.text
    print(data)


if __name__ == "__main__":
    geocode_poi()