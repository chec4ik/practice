@echo off
call conda init
call conda activate myenv
python gui.py
pause