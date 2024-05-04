import subprocess
import os





def run_bat_file():
    config_file_path = 'long_video_transfer\\audio.conf'  # 替换为你的配置文件路径
    current_directory = os.getcwd()  # 获取当前文件夹路径
    # 构建要写入的路径
    path_to_write = os.path.join(current_directory, 'long_video_transfer\\test.wav')
    # 要写入的内容
    content_to_write = f"{path_to_write}"
    # 打开文件以追加模式
    with open(config_file_path, 'w') as f:
        f.write(content_to_write)
    try:
        # 使用 subprocess 调用批处理文件
        path_to_run = os.path.join(current_directory, 'long_video_transfer\\run_transfer.bat')
        print(path_to_run)
        converted_path = path_to_run.replace('\\', '\\\\')
        print(converted_path)
        # 'E:\\Python\\project\\Vivo_AIGC\\aigc_api_test\\long_video_transfer\\run_transfer.bat'
        print(type(path_to_run))
        # subprocess.run(path_to_run, shell=True, check=True)
        os.system("cmd /c" + converted_path)
        print("批处理文件成功执行。")
    except subprocess.CalledProcessError as e:
        print("批处理文件执行失败:", e)


# run_bat_file()
#
