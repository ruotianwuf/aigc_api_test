# encoding: utf-8
import uuid
import time
import requests
from openai import OpenAI
from work_careeradvice.auth_util import gen_sign_headers

message = []


def sync_vivogpt_careeradvice(ask):
    # APP_ID = '3032660331'
    # APP_KEY = 'LxpYKtKbgakYmMTN'
    # URI = '/vivogpt/completions'
    # DOMAIN = 'api-ai.vivo.com.cn'
    #
    # message.append({"content": ask, "role": "user"})
    # print(message)
    # METHOD = 'POST'
    #
    # params = {
    #     'requestId': str(uuid.uuid4())
    # }
    # print('requestId:', params['requestId'])
    #
    # data = {
    #     'messages': message,
    #     'model': 'vivo-BlueLM-TB',
    #     'sessionId': str(uuid.uuid4()),
    #     'extra': {
    #         'temperature': 0.95
    #     },
    #     'systemPrompt': '你的中文名字叫职业规划助手，当回复问题时需要回复你的名字时，中文名必须回复职业规划小助手，此外回复和你的名字相关的问题时，也需要给出和你的名字对应的合理回复。当回复职业规划与未来建议时，需要结合给出的专业、学历、年龄、性别、职业意向等来给出对应的推荐，列出不少于5个具体的职业类型，介绍这个职业需要的知识、大致薪资待遇（以月薪或者年薪，单位为人民币）等内容,分析这个职业的优势与不足，尽可能给出详细的描述，最后要给予适当的建议与鼓励。'
    # }
    # print(data)
    # headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)
    # headers['Content-Type'] = 'application/json'
    #
    # start_time = time.time()
    # url = 'https://{}{}'.format(DOMAIN, URI)
    # response = requests.post(url, json=data, headers=headers, params=params)
    #
    # if response.status_code == 200:
    #     res_obj = response.json()
    #     print(f'response:{res_obj}')
    #     if res_obj['code'] == 0 and res_obj.get('data'):
    #         content = res_obj['data']['content']
    #         print(f'final content:\n{content}')
    #         message.append({"content": content, "role": "assistant"})
    #         print(message)
    #         return content
    # else:
    #     print(response.status_code, response.text)
    # end_time = time.time()
    # timecost = end_time - start_time
    # print('请求耗时: %.2f秒' % timecost)

# if __name__ == '__main__':
#     sync_vivogpt_careeradvice('专业：；学历：学历；性别：性别；年龄；就业意向：')

    client = OpenAI(
        api_key="sk-pqCSh75OiautBU5yfgGcZTv399xqsDz75RCRmcaltXgIFNlB",  # 在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
        base_url="https://api.moonshot.cn/v1",
    )

    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system",
             "content": "你的中文名字叫职业规划助手，当回复问题时需要回复你的名字时，中文名必须回复职业规划小助手，此外回复和你的名字相关的问题时，也需要给出和你的名字对应的合理回复。当回复职业规划与未来建议时，需要结合给出的专业、学历、年龄、性别、职业意向等来给出对应的推荐，列出不少于5个具体的职业类型，介绍这个职业需要的知识、大致薪资待遇（以月薪或者年薪，单位为人民币）等内容,分析这个职业的优势与不足，尽可能给出详细的描述，最后要给予适当的建议与鼓励。"},
            {"role": "user", "content": ask}
        ],
        temperature=0.3,
    )

    # 通过 API 我们获得了 Kimi 大模型给予我们的回复消息（role=assistant）
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content
