# encoding: utf-8
#ASR->70B->TTS
import uuid
import time
import requests

from work_interview.auth_util import gen_sign_headers


def sync_vivogpt_interview_writting(ask):
    message = []
    questions = []
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
        'systemPrompt': '你是一位面试官，在获得用户的信息之后，需要根据用户的具体专业和应聘岗位，提出有关专业知识、业务基础等方面的内容，问题类型为概念辨析题、实际应用题、创新思维题、个人见解题等，但是回答里面不需要给出问题类型，总共需要5个题目，给出序号和题干'
    }
    print(data)
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
            print(f'message:{message}')

            # 将内容解析为单个问题
            questions_list = content.strip().split('\n')
            for q in questions_list:
                if q.strip():
                    parts = q.split(' ', 1)
                    if len(parts) == 2:
                        number, text = parts
                        questions.append({
                            'title': f'问题 {number}',
                            'text': text.strip(),
                            'answer': ''
                        })
            print(questions)
            return questions
    else:
        print(response.status_code, response.text)
    end_time = time.time()
    timecost = end_time - start_time
    print('请求耗时: %.2f秒' % timecost)

# if __name__ == '__main__':
#     sync_vivogpt_interview_writting('软件设计师')

def sync_vivogpt_interview_writting_answers(answers):
    APP_ID = '3032660331'
    APP_KEY = 'LxpYKtKbgakYmMTN'
    URI = '/vivogpt/completions'
    DOMAIN = 'api-ai.vivo.com.cn'
    METHOD = 'POST'
    DELAY = 5  # 每次提交后的延迟时间，单位：秒

    final_evaluation = []
    i = 1
    for ans in answers:
        if 'title' in ans and 'text' in ans and 'answer' in ans:
            print("<-----分割线----->")
            if not ans['answer']:
                ans['answer'] = "此题未作答"
            content = f"{ans['title']} {ans['text']} 答案: {ans['answer']}"
            messages = [{"content": content, "role": "user"}]

            params = {
                'requestId': str(uuid.uuid4())
            }

            data = {
                'messages': messages,
                'model': 'vivo-BlueLM-TB',
                'sessionId': str(uuid.uuid4()),
                'systemPrompt': ('你的中文名字叫蓝心面试助手，当回复问题时需要回复你的名字时，中文名必须回复蓝心面试助手，'
                                 '此外回复和你的名字相关的问题时，也需要给出和你的名字对应的合理回复。你的工作部分是对给出的回答进行评分，评分范围为0-10，格式为当前分数/10（比如得分为9分，就输出：9/10），并对每道题给出适当的评价，如果问题的答案是“此题未作答”，直接判为0分'),
                'extra': {
                    'temperature': 0.7,
                }
            }

            headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)
            headers['Content-Type'] = 'application/json'

            print(f"Sending question: {content}")

            start_time = time.time()
            url = 'https://{}{}'.format(DOMAIN, URI)
            response = requests.post(url, json=data, headers=headers, params=params)
            if response.status_code == 200:
                res_obj = response.json()
                if res_obj['code'] == 0 and res_obj.get('data'):
                    evaluation = f"题号 {i}: {res_obj['data']['content']}"
                    final_evaluation.append(evaluation)
                else:
                    print(f'Error in response content: {res_obj}')
                    final_evaluation.append("部分评价失败")
            else:
                print(f'Response status code: {response.status_code}')
                print(f'Response text: {response.text}')
                final_evaluation.append("部分评价失败")

            end_time = time.time()
            timecost = end_time - start_time
            print('请求耗时: %.2f秒' % timecost)

            i += 1
            # 添加延迟
            time.sleep(DELAY)
        else:
            print(f"Invalid answer structure: {ans}")

    return "\n".join(final_evaluation)

# if __name__ == '__main__':
#     answers = [
#         {"title": "问题 1", "text": "请解释软件工程的基本概念，并列举一些常用的软件工程方法。",
#          "answer": "软件工程是计算机科学的一个分支，涉及软件开发、维护和管理的系统方法。常用的软件工程方法包括瀑布模型、敏捷开发、螺旋模型和V模型等。"},
#         {"title": "问题 2", "text": "请描述面向对象编程的四大特性，并举例说明每个特性。",
#          "answer": ""},
#         {"title": "问题 3", "text": "请解释常见的数据结构及其优缺点，如数组、链表、栈、队列、树和图。",
#          "answer": "数组是一种连续存储的数据结构，优点是可以快速访问，缺点是大小固定；链表是一种非连续存储的数据结构，优点是动态调整大小，缺点是访问速度较慢；栈是一种LIFO结构，适用于递归算法实现；队列是一种FIFO结构，适用于任务调度；树是一种分层结构，适用于表示层级关系的数据；图是一种网络结构，适用于表示复杂的关系。"},
#         {"title": "问题 4", "text": "请解释数据库的基本概念，并描述常见的数据库模型及其特点。",
#          "answer": "数据库是一个有组织的数据集合，旨在有效地存储、检索和管理数据。常见的数据库模型包括关系模型、层次模型和网络模型。关系模型基于表格结构，支持SQL查询；层次模型基于树形结构，适用于描述层级关系的数据；网络模型基于图结构，适用于描述复杂的多对多关系。"},
#         {"title": "问题 5", "text": "请解释大数据的概念，并描述大数据技术的常见应用场景。",
#         "answer": "大数据是指那些超出了传统数据处理工具处理能力的数据集合。大数据技术包括数据采集、存储、处理和分析。常见的大数据应用场景包括商业智能、用户行为分析、科学研究、智能制造和金融风控等。"},
#
#     ]
#
#     evaluation = sync_vivogpt_interview_writting_answers(answers)
#     print(evaluation)