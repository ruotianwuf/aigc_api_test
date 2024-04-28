import requests
import json
data = json.dumps({
    'username': '11',
    'password': '2222',
})
response = requests.post(url='http://127.0.0.1:5000/adduser/student/1', data=data)
print(response.text)
