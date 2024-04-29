import requests
import json
data = json.dumps({
    'username': "11",
})
response = requests.post(url='http://127.0.0.1:5000/student/forum/getPost', data=data)
print(response.text)
