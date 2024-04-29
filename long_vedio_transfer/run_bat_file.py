import subprocess

def run_bat_file():
    file_path='E:\\Python\\project\\Vivo_AIGC\\aigc_api_test\\long_vedio_transfer\\run_transfer.bat'
    try:
        # 使用 subprocess 调用批处理文件
        subprocess.run(file_path, shell=True, check=True)
        print("批处理文件成功执行。")
    except subprocess.CalledProcessError as e:
        print("批处理文件执行失败:", e)


run_bat_file()
# 示例用法
# bat_file_path = "your_bat_file.bat"  # 你的批处理文件路径
# run_bat_file(bat_file_path)
