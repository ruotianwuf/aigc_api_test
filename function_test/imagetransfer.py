
import io
import requests
import json

from PIL import Image
import base64

from werkzeug.utils import secure_filename

from controller.UserServerController import UserServerController



def image_to_base64(image_path):
    # 打开图片文件
    with Image.open(image_path) as img:
        # 创建一个字节流对象
        img_byte_arr = io.BytesIO()
        # 将图片保存到字节流中，这里使用PNG格式以保留透明度
        if img.mode == 'RGBA':
            img = img.convert('RGBA')  # 确保图像是RGBA模式
            img.save(img_byte_arr, format='PNG')
        else:
            img.save(img_byte_arr, format='PNG')

        # 重置字节流对象的位置指针到开始位置
        img_byte_arr.seek(0)

        # 获取字节流中的二进制数据
        img_byte_arr = img_byte_arr.getvalue()

        # 使用base64库将二进制数据编码为Base64格式
        base64_image = base64.b64encode(img_byte_arr).decode('utf-8')

    return base64_image

image_path1 = '../static/humanphoto/ljy18482245211.png'
base64_image1 = image_to_base64(image_path1)
data = {'blob': base64_image1}
con = UserServerController()
res = con.insert_blob_ServerStatus('ljy', data)
print(res)


img1 = con.find_blob_ServerStatus(1)
img1 = json.loads(img1[0][0])
base64_image1 = img1['blob']
image_path2 = '../static/humanphoto/test.png'
base64_image2 = image_to_base64(image_path2)
# base64_image1 = con.find_blob_ServerStatus(data)
# base64_image1 = base64_image1[0][0]
# base64_image1 = base64_image1.decode('utf-8')
# print(base64_image1)

params_str = [
                    {
                        "image": base64_image1,
                        "image_type": "BASE64",
                        "face_type": "LIVE",
                        "quality_control": "LOW"
                    },
                    {
                        "image": base64_image2,
                        "image_type": "BASE64",
                        "face_type": "LIVE",
                        "quality_control": "LOW"
                    }
                ]
print(type(params_str))

# params_str = json.dumps(params_str, ensure_ascii=True)
# print(type(params_str))
request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"

host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=n6MEdq40kQfFINA5J0cC4rLu&client_secret=Hz91ksY1oVVob4MAis9QycbfXR1IfKzJ'
response = requests.get(host)
if response:
    print(type(response.json()))
at = response.json()
access_token = at['access_token']
request_url = request_url + "?access_token=" + access_token
print(request_url)
headers = {'content-type': 'application/json'}
response = requests.post(request_url, json=params_str, headers=headers)
if response:
    result = response.json()
    print(result['result']['score'])
    num = int(result['result']['score'])