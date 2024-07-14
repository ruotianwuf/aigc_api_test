# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import random

# 创信_验证类短信接口 Python示例代码
if __name__ == '__main__':
    url = 'http://gwgp-wtxhytukujk.n.bdcloudapi.com/chuangxin/dxjk'
    params = {}
    random_number = random.randint(1000,9999)
    params['content'] = '【智慧平台】你的验证码是：'+ str(random_number)
    params['mobile'] = '18482245211'

    headers = {

        'Content-Type': 'application/json;charset=UTF-8',
        'X-Bce-Signature': 'AppCode/2cb34f818c284133869066bc2ac4cb76'
    }
    r = requests.request("GET", url, params=params, headers=headers)
    print(r.content)
