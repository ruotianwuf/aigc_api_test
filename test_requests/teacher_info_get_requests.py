import requests
import json
data = json.dumps({
    'city': "成都",
})
response = requests.post(url='http://127.0.0.1:2750/travel_answer', data=data)
print(response.text)
