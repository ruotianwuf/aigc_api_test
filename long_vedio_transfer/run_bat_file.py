import subprocess
import os


def write_path_to_conf_file():
    config_file_path = 'audio.conf'  # 替换为你的配置文件路径
    current_directory = os.getcwd()  # 获取当前文件夹路径
    # 构建要写入的路径
    path_to_write = os.path.join(current_directory, 'test.wav')
    # 要写入的内容
    content_to_write = f"{path_to_write}"
    # 打开文件以追加模式
    with open(config_file_path, 'w') as f:
        f.write(content_to_write)

# 调用函数写入路径到配置文件中



def run_bat_file():
    write_path_to_conf_file()
    # file_path='E:\\Python\\project\\Vivo_AIGC\\aigc_api_test\\long_vedio_transfer\\run_transfer.bat'
    try:
        # 使用 subprocess 调用批处理文件
        # subprocess.run(file_path, shell=True, check=True)
        os.system("cmd /c run_transfer.bat")
        print("批处理文件成功执行。")
    except subprocess.CalledProcessError as e:
        print("批处理文件执行失败:", e)


run_bat_file()
# 示例用法
# bat_file_path = "your_bat_file.bat"  # 你的批处理文件路径
# run_bat_file(bat_file_path)
