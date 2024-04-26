import requests
import json
data = json.dumps({
    'question': "分析图片" + "../static/img/img.png",
})
response = requests.post(url='http://127.0.0.1:5000/answer', data=data)
print(response.text)
