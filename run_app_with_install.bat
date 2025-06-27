@echo off
cd /d %~dp0

echo Install in process...
pip install -r requirements.txt

echo.
echo Join App:
python main.py

pause
