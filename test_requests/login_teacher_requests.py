import requests
import json
data = json.dumps({
    'username': 'sl',
    'password': '1111',
})
response = requests.post(url='http://127.0.0.1:5000/login/teacher/1', data=data)
print(response.text)
