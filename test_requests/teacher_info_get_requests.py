import requests
import json
import datetime
data = json.dumps({
    "data": "1"
})
response = requests.post(url='http://127.0.0.1:2750/getchatmanmsg', data=data)
print(response.text)
