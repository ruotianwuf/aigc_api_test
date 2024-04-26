import requests
import json
data = json.dumps({
    'question': "我需要旅游资讯",
})
response = requests.post(url='http://127.0.0.1:5000/answer_msg', data=data)
print(response.text)