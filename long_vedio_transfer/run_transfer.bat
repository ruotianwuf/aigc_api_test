@echo off


cd /d " E:\Python\project\Vivo_AIGC\aigc_api_test>"
@echo off


call .venv\Scripts\activate

python long_vedio_transfer/ai_fileasr_client.py long_vedio_transfer/audio.conf


timeout /t 120 /nobreak  >nul


python long_vedio_transfer\long_vedio_api_get.py

exit