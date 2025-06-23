@echo off
call venv\Scripts\activate.bat
cd pipeline
python main.py --help
cd ..
pause