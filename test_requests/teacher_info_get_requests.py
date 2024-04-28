import requests
import json
data = json.dumps({
    'username': "sl",
})
response = requests.post(url='http://127.0.0.1:5000/teacher/info/get', data=data)
print(response.text)
