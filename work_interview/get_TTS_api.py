# -*- coding: utf-8 -*-
from websocket import create_connection, ABNF
import time
from work_interview.auth_util import gen_sign_headers
import base64
import json
import io
import wave
import os
from enum import IntEnum

class AueType(IntEnum):
    PCM = 0
    OPUS = 1

class TTS(object):
    def __init__(self, app_id=None, app_key=None, engineid='short_audio_synthesis_jovi', *args, **argskw):
        self._appid = app_id or os.getenv('APP_ID')
        self._app_key = app_key or os.getenv('APP_KEY')
        self._engineid = engineid
        self._ws = None

    def open(self, domain="wss://api-ai.vivo.com.cn"):
        uri = "/tts"
        system_time = str(int(time.time()))
        user_id = 'userX'
        model = 'modelX'
        product = 'productX'
        package = 'packageX'
        client_version = '0'
        system_version = '0'
        sdk_version = '0'
        android_version = '9'
        params = {
            "engineid": self._engineid, "system_time": system_time, "user_id": user_id, "model": model,
            "product": product, "client_version": client_version, "system_version": system_version,
            "package": package, "sdk_version": sdk_version, "android_version": android_version
        }
        headers = gen_sign_headers(app_id=self._appid, app_key=self._app_key, method='GET', uri=uri, query=params)
        headers["vaid"] = "123456789"
        param_str = '?'
        seq = ''
        for key, value in params.items():
            param_str = param_str + seq + key + '=' + value
            seq = '&'
        url = domain + uri + param_str
        try:
            self._ws = create_connection(url, header=headers)
        except Exception as e:
            return None
        code, data = self._ws.recv_data(True)
        return self._ws

    def gen_radio(self, text='你好', vcn='xiaofu', aue=AueType.PCM, extra={}):
        if self._ws is None:
            return None
        obj = {}
        obj["speed"] = 60
        obj["text"] = base64.b64encode(text.encode('utf-8')).decode('utf-8')
        obj["auf"] = 'audio/L16;rate=24000'
        obj["vcn"] = vcn
        obj["volume"] = 30
        obj["aue"] = aue
        obj["sfl"] = 1
        obj["reqId"] = int(round(time.time() * 1000))
        obj.update(extra)
        self._ws.send(json.dumps(obj))
        audio_buff = b''
        while True:
            code, data = self._ws.recv_data(True)
            if code == ABNF.OPCODE_PONG:
                pass
            elif code == ABNF.OPCODE_CLOSE:
                return None
            elif code == ABNF.OPCODE_TEXT:
                jre = json.loads(data)
                if jre["error_code"] != 0:
                    return None
                else:
                    if 'data' not in jre:
                        continue
                    audio = base64.b64decode(jre["data"]["audio"])
                    audio_buff += audio
                    if jre["data"]["status"] == 2:
                        break
            else:
                break
        return audio_buff

class ShortTTS(object):
    vivoHelper = "vivoHelper"
    yunye = "yunye"
    wanqing = "wanqing"
    xiaofu = "xiaofu"
    yige_child = "yige_child"
    yige = "yige"
    yiyi = "yiyi"
    xiaoming = "xiaoming"

class LongTTS(object):
    x2_vivoHelper = "vivoHelper"
    x2_yige = "x2_yige"
    x2_yige_news = "x2_yige_news"
    x2_yunye = "x2_yunye"
    x2_yunye_news = "x2_yunye_news"
    x2_M02 = "x2_M02"
    x2_M05 = "x2_M05"
    x2_M10 = "x2_M10"
    x2_F163 = "x2_F163"
    x2_F25 = "x2_F25"
    x2_F22 = "x2_F22"
    x2_F82 = "x2_F82"

def pcm2wav(pcmdata: bytes, channels=1, bits=16, sample_rate=24000):
    if bits % 8 != 0:
        raise ValueError("bits % 8 must == 0. now bits:" + str(bits))
    io_fd = io.BytesIO()
    wavfile = wave.open(io_fd, 'wb')
    wavfile.setnchannels(channels)
    wavfile.setsampwidth(bits // 8)
    wavfile.setframerate(sample_rate)
    wavfile.writeframes(pcmdata)
    wavfile.close()
    io_fd.seek(0)
    return io_fd

def get_tts_instance(engine_id='short_audio_synthesis_jovi'):
    input_params = {
        'app_id': os.getenv('APP_ID', '3032660331'),
        'app_key': os.getenv('APP_KEY', 'LxpYKtKbgakYmMTN'),
        'engineid': engine_id
    }
    return TTS(**input_params)
