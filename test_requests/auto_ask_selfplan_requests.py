import requests
import json
data = json.dumps({
    'username': '11',
})
response = requests.post(url='http://127.0.0.1:5000/answer_msg/advice', data=data)
print(response.text)
