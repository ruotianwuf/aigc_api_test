# encoding: utf-8
import uuid
import time
import requests
from work_careeradvice.auth_util import gen_sign_headers
from openai import OpenAI

message = []

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
#         'temperature': 0.9
#     },
#     'systemPrompt': '你的中文名字叫未来学习计划助手，当回复问题时需要回复你的名字时，中文名必须回复未来学习计划助手，此外回复和你的名字相关的问题时，也需要给出和你的名字对应的合理回复。当给你传输和学生课程和学习情况的时候，只生成对应且合理的学习计划。并且成绩是A+最好其余依次向下。内容必须准确有可行性、且内容必须详细'
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
#
# end_time = time.time()
# timecost = end_time - start_time
# print('请求耗时: %.2f秒' % timecost)

# sync_vivogpt_msg('你好')
client = OpenAI(
    api_key="sk-Pyi6EzKmSZP79YjIWvjaWvYB2MP6P3zNqY2ce6Fe4XLiiXx6",  # 在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
    base_url="https://api.moonshot.cn/v1",
)

# 我们定义一个全局变量 messages，用于记录我们和 Kimi 大模型产生的历史对话消息
# 在 messages 中，既包含我们向 Kimi 大模型提出的问题（role=user），也包括 Kimi 大模型给我们的回复（role=assistant）
# 当然，也包括初始的 System Prompt（role=system）
# messages 中的消息按时间顺序从小到大排列
messages = [
    {"role": "system",
     "content": "你的中文名字叫未来学习计划助手，当回复问题时需要回复你的名字时，中文名必须回复未来学习计划助手，此外回复和你的名字相关的问题时，也需要给出和你的名字对应的合理回复。当给你传输和学生课程和学习情况的时候，只生成对应且合理的学习计划。并且成绩是A+最好其余依次向下。内容必须准确有可行性、且内容必须详细'"},
]


def chat(input: str) -> str:
    """
    chat 函数支持多轮对话，每次调用 chat 函数与 Kimi 大模型对话时，Kimi 大模型都会”看到“此前已经
    产生的历史对话消息，换句话说，Kimi 大模型拥有了记忆。
    """

    # 我们将用户最新的问题构造成一个 message（role=user），并添加到 messages 的尾部


    messages.append({
        "role": "user",
        "content": input,
    })

# 携带 messages 与 Kimi 大模型对话
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=messages,
        temperature=0.3,
    )

# 通过 API 我们获得了 Kimi 大模型给予我们的回复消息（role=assistant）
    assistant_message = completion.choices[0].message

# 为了让 Kimi 大模型拥有完整的记忆，我们必须将 Kimi 大模型返回给我们的消息也添加到 messages 中
    messages.append(assistant_message)

    return assistant_message.content

    print(chat("你好，我今年 27 岁。"))
    print(chat("你知道我今年几岁吗？"))  # 在这里，Kimi 大模型根据此前的上下文信息，将会知道你今年的年龄是 27 岁



# sync_vivogpt_msg('你好')

