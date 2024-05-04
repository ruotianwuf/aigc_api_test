@echo off

set "batch_dir=%~dp0"

cd /d "%batch_dir%"

call ..\.venv\Scripts\activate

python ai_fileasr_client.py audio.conf

timeout /t 120 /nobreak >nul

python long_vedio_api_get.py

exit