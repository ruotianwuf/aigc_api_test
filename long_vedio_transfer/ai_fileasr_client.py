import requests
import json
import sys
import time
import uuid
from urllib import parse


from auth_util import gen_sign_headers

headers = {"Content-Type": "application/json"}

g_session = requests.Session()

SLICE_LEN = 5 * 1024 * 1024

domain = 'api-ai.vivo.com.cn/lasr'

appid = '3032660331'
appkey = 'LxpYKtKbgakYmMTN'

AUDIO_API_URL = "http://" + domain

audio_type = "auto"
# audio_type = "pcm"


def create_params(interface, audio_id=None, x_session_id=None, slice_index=None):
    t = int(round(time.time() * 1000))

    params = {'client_version': parse.quote('2.0'), 'package': parse.quote('pack'),
              'user_id': parse.quote('2addc42b7ae689dfdf1c63e220df52a2'), 'system_time': parse.quote(str(t)),
              'net_type': 1, 'engineid': "fileasrrecorder"}

    if interface == '/lasr/upload':
        params['audio_id'] = audio_id
        params['x-sessionId'] = x_session_id
        params['slice_index'] = str(slice_index)

    headers = gen_sign_headers(appid, appkey, 'POST', interface, params)

    param_str = ''
    seq = ''

    for key, value in params.items():
        value = str(value)
        param_str = param_str + seq + key + '=' + value
        seq = '&'

    return param_str, headers


def http_chunk_upload(audio_data, audio_id, x_session_id, slice_index):
    try:
        boundary = ''.join(str(uuid.uuid1()).split('-'))
        reqbody = bytes("------------------------------" + boundary + "\r\n", "utf-8")
        reqbody = reqbody + bytes('Content-Disposition: form-data; name="file"; filename="' + "test.wav" + '"\r\n',
                                  "utf-8")
        reqbody = reqbody + bytes("Content-Type: application/octet-stream\r\n\r\n", "utf-8")
        reqbody = reqbody + audio_data + bytes("\r\n", "utf-8")
        reqbody = reqbody + bytes("------------------------------" + boundary + "--\r\n", "utf-8")

        param_str, headers = create_params('/lasr/upload', audio_id=audio_id, x_session_id=x_session_id,
                                           slice_index=slice_index)
        headers["Accept"] = "*/*"
        headers["Content-Type"] = "multipart/form-data; boundary=----------------------------" + boundary

        requrl = AUDIO_API_URL + "/upload?" + param_str
        resp = g_session.post(
            requrl,
            data=reqbody,
            headers=headers)

        return resp

    except Exception as e:
        return dict(status_code=502, text=str(e))


def task_create(audio_file, x_session_id, audio_type):
    audio_file.seek(0, 2)
    size = audio_file.tell()

    slice_num, other = divmod(size, SLICE_LEN)
    if other > 0: slice_num += 1
    print('audio slice_num:', slice_num, 'audio size:', size, 'x-sessionId:', x_session_id)

    post_body = {
        "audio_type": audio_type,
        "x-sessionId": x_session_id,
        "slice_num": slice_num
    }

    param_str, headers = create_params('/lasr/create')
    headers["Content-Type"] = "application/json; charset=UTF-8"

    requrl = AUDIO_API_URL + "/create?" + param_str

    resp = g_session.post(
        requrl,
        data=json.dumps(post_body),
        headers=headers)
    print(resp.json())

    try:
        if resp.status_code == 200:
            retobj = resp.json()

            if retobj:
                errno = retobj["action"]
                if errno == "error":
                    return 1, retobj["desc"], slice_num
                else:
                    return 0, retobj['data']["audio_id"], slice_num
            else:
                return 1, resp.text, slice_num

        else:
            return resp.status_code, resp.text, slice_num

    except Exception as e:
        print("task_create err", repr(e))
        return 1, str(e), slice_num


def task_upload(audio_id, audio_file, n_slices, x_session_id):
    slice_index = 0

    while slice_index < n_slices:
        audio_file.seek(slice_index * SLICE_LEN)
        slice_data = audio_file.read(SLICE_LEN)

        resp = http_chunk_upload(slice_data, audio_id, x_session_id, slice_index)
        if resp.status_code == 200:
            json = resp.json()
            if json:
                errno = json["action"]
                if errno == "error":
                    print('[ERR] status:', 1, 'message:', json['desc'], file=sys.stderr)
                    break
                else:
                    print('slice_index:', slice_index, 'sid:', json['sid'], json['data'])
                    slice_index += 1
            else:
                print('[ERR] status:', 1, 'message:', resp.text, file=sys.stderr)
                break
        else:
            print('[ERR] status:', resp.status_code, 'message:', resp.text, file=sys.stderr)
            break


def task_run(x_session_id, audio_id):
    post_body = {
        "audio_id": audio_id,
        "x-sessionId": x_session_id
    }

    param_str, headers = create_params('/lasr/run')
    headers["Content-Type"] = "application/json; charset=UTF-8"
    requrl = AUDIO_API_URL + "/run?" + param_str

    resp = g_session.post(
        requrl,
        data=json.dumps(post_body),
        headers=headers)

    print(resp.json())
    return resp.json()


def task_progress(x_session_id, task_id):
    post_body = {
        "task_id": task_id,
        "x-sessionId": x_session_id
    }

    param_str, headers = create_params('/lasr/progress')
    headers["Content-Type"] = "application/json; charset=UTF-8"
    requrl = AUDIO_API_URL + "/progress?" + param_str

    resp = g_session.post(
        requrl,
        data=json.dumps(post_body),
        headers=headers)

    print(resp.json())
    return resp.json()


def task_result(x_session_id, task_id):
    post_body = {
        "task_id": task_id,
        "x-sessionId": x_session_id
    }

    param_str, headers = create_params('/lasr/result')
    headers["Content-Type"] = "application/json; charset=UTF-8"
    requrl = AUDIO_API_URL + "/result?" + param_str

    resp = g_session.post(
        requrl,
        data=json.dumps(post_body),
        headers=headers)

    result = json.dumps(resp.json(), ensure_ascii=False)
    return result


def main():
    if len(sys.argv) < 2:
        print('usage :  python %s conf' % sys.argv[0])
        print('example: python %s %s' % (sys.argv[0], 'audio.conf'))
        sys.exit(1)
    else:
        config = sys.argv[1]

    print("start time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    start_time = time.time()

    with open(config, 'rt') as f:
        line = f.readline()
    try:
        line = line.strip()
        audio_file = open(line, 'rb')

        print('<===task create start===>')
        x_session_id = ''.join(str(uuid.uuid1()).split('-'))
        err, audio_id, slice_num = task_create(audio_file, x_session_id, audio_type)
        if err:
            print('[ERR] task_create audio status:', err, 'message:', audio_id, file=sys.stderr)
            return
        print('<===task create end===>')

        print('<===task upload start===>')
        task_upload(audio_id, audio_file, slice_num, x_session_id)
        print('<===task upload end===>')

        print('<===task run start===>')
        task_run_result = task_run(x_session_id, audio_id)
        task_id = task_run_result["data"]["task_id"]
        print('<===task run end===>')

        print('<===task progress start===>')
        progress = 0
        progress_result = ""
        while progress != 100:
            time.sleep(2)
            progress_result = task_progress(x_session_id, task_id)
            progress = progress_result["data"]["progress"]
        print('<===task progress end===>')

        print('<===task result start===>')
        task_result_result = task_result(x_session_id, task_id)
        print("内容"+task_result_result)

        # content = sync_vivogpt(task_result_result)
        # 将结果写入到文件
        with open('E:\\Python\\project\\Vivo_AIGC\\aigc_api_test\\long_vedio_transfer\\output.txt', 'w', encoding='utf-8') as f:
            print("正在写入")
            f.write("内容：" + str(task_result_result))
            print("写入完成")
        print('<===task result end===>')

    except Exception as e:
        print(str(e))
        return

    print("end time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    end_time = time.time()
    print("all costtime: {:.2f}s".format(end_time - start_time))
    # print(content)


if __name__ == "__main__":
    main()
