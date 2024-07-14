#!/usr/bin/env python
# encoding: utf-8

import requests
import base64
from work_careeradvice.auth_util import gen_sign_headers

# 请注意替换APP_ID、APP_KEY、PIC_FILE
APP_ID = '3032660331'
APP_KEY = 'LxpYKtKbgakYmMTN'
DOMAIN = 'api-ai.vivo.com.cn'
URI = '/ocr/general_recognition'
METHOD = 'POST'
PIC_FILE = '../static/img/img_1.png'


def ocr_test():
    picture = PIC_FILE
    with open(picture, "rb") as f:
        b_image = f.read()
    image = base64.b64encode(b_image).decode("utf-8")
    post_data = {"image": image, "pos": 2, "businessid": "1990173156ceb8a09eee80c293135279"}
    params = {}
    headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)

    url = 'http://{}{}'.format(DOMAIN, URI)
    response = requests.post(url, data=post_data, headers=headers)
    if response.status_code == 200:
        print(response.json())
    else:
        print(response.status_code, response.text)


if __name__ == '__main__':
    ocr_test()