import json

from flask import Flask, request, jsonify, render_template

from api_project_get.get_api import sync_vivogpt

app = Flask(__name__)

# 处理根路径请求，返回欢迎页面
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/answer', methods=['POST'])
def getanswer():
    data = json.loads(request.get_data(as_text=True))
    data = data['question']
    result = sync_vivogpt(data)
    if result != None:
        return jsonify({'success': True, 'result': result}), 200
    else:
        return jsonify({'success': False}), 200




if __name__ == '__main__':
    app.run(debug=True)
