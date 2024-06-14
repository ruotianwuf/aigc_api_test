# -*- coding: utf-8 -*-
from websocket import create_connection, ABNF
import time
from auth_util import gen_sign_headers
import base64
import json
import os
from enum import IntEnum


# os.environ['APP_ID']=your_app_id
# os.environ['APP_KEY']=your_app_key


class AueType(IntEnum):
    PCM = 0
    OPUS = 1


class TTS(object):

    def __init__(
        self,
        app_id=None,
        app_key=None,
        engineid="short_audio_synthesis_jovi",
        *args,
        **argskw,
    ):
        self._appid = app_id or os.getenv("APP_ID")
        self._app_key = app_key or os.getenv("APP_KEY")
        if isinstance(self._app_key, str):
            self._app_key = self._app_key
        self._engineid = engineid
        self._ws = None

    def open(self, domain="wss://api-ai.vivo.com.cn"):
        uri = "/tts"
        system_time = str(int(time.time()))
        user_id = "userX"
        model = "modelX"
        product = "productX"
        package = "packageX"
        client_version = "0"
        system_version = "0"
        sdk_version = "0"
        android_version = "9"
        params = {
            "engineid": self._engineid,
            "system_time": system_time,
            "user_id": user_id,
            "model": model,
            "product": product,
            "client_version": client_version,
            "system_version": system_version,
            "package": package,
            "sdk_version": sdk_version,
            "android_version": android_version,
        }
        headers = gen_sign_headers(
            app_id=self._appid,
            app_key=self._app_key,
            method="GET",
            uri=uri,
            query=params,
        )
        headers["vaid"] = "123456789"
        param_str = "?"
        seq = ""
        for key, value in params.items():
            param_str = param_str + seq + key + "=" + value
            seq = "&"
        url = domain + uri + param_str
        print(url)
        try:
            self._ws = create_connection(url, header=headers)
        except Exception as e:
            print("print err:", repr(e))
            return None
        # get first handshake data
        code, data = self._ws.recv_data(True)
        return self._ws

    def gen_radio(self, text="你好", vcn="xiaofu", aue=AueType.PCM, extra={}):
        if self._ws is None:
            return None
        obj = {}
        obj["speed"] = 60
        obj["text"] = base64.b64encode(text.encode("utf-8")).decode("utf-8")
        obj["auf"] = "audio/L16;rate=24000"
        obj["vcn"] = vcn
        obj["volume"] = 30
        obj["aue"] = aue
        obj["sfl"] = 1
        obj["reqId"] = int(round(time.time() * 1000))  # int(t.ident)
        obj.update(extra)
        self._ws.send(json.dumps(obj))
        print("finish_send_text", json.dumps(obj))
        audio_buff = b""
        while True:
            code, data = self._ws.recv_data(True)
            if code == ABNF.OPCODE_PONG:
                # recv pong
                pass
            elif code == ABNF.OPCODE_CLOSE:
                # recv close
                print("close")
                return None
            elif code == ABNF.OPCODE_TEXT:
                # recv text
                jre = json.loads(data)
                if jre["error_code"] != 0:
                    print(f"error_code is not zero. data:{data}")
                    return None
                else:
                    if "data" not in jre:
                        print(jre)
                        continue
                    audio = base64.b64decode(jre["data"]["audio"])
                    audio_buff += audio
                    if jre["data"]["status"] == 0:
                        print("the first data")
                    elif jre["data"]["status"] == 2:
                        print("complete ~")
                        break
                    jre["data"]["audio"] = ""
                    print(jre)
            else:
                print("error,recv type:", code)
                break
        return audio_buff


if __name__ == "__main__":
    input_params = {
        "app_id": "3032660331",
        "app_key": "LxpYKtKbgakYmMTN",
        "engineid": "long_audio_synthesis_screen",
    }
    tts = TTS(**input_params)
    tts.open()
    audio_buffer = tts.gen_radio(vcn="x2_F82")
    print(len(audio_buffer))
