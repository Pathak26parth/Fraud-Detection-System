@echo off
echo Starting Spam Detection AI Model Service...
cd /d "%~dp0DAIICT_FinalModel"
python serve.py
