@echo off

set "batch_dir=%~dp0"

cd /d "%batch_dir%"

call ..\venv\Scripts\activate

REM 添加模块所在的目录到 PYTHONPATH 环境变量中
set MODULE_PATH=%cd%\..\api_project_get
set PYTHONPATH=%MODULE_PATH%;%PYTHONPATH%

python ai_fileasr_client.py audio.conf

timeout /t 120 /nobreak >nul

python long_video_api_get.py

exit
