import requests
import json
data = json.dumps({
    'username': "sl",
})
response = requests.post(url='http://127.0.0.1:5000/teacher/republic/get_sinfo', data=data)
print(response.text)
