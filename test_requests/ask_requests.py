import requests
import json
data = json.dumps({
    'question': '写一首关于成都的诗歌',
})
response = requests.post(url='http://127.0.0.1:5000/answer', data=data)
print(response.text)
