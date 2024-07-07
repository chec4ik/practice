@echo off
call conda init
call conda activate myenv
pip install -r requirements.txt
pause