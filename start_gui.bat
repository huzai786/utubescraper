@echo off

python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed on this system.
    exit /b 1
)

if not exist env\Scripts\activate.bat (
    echo Creating virtual environment 'env'...
    python -m venv env
    call env\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
    deactivate
)

call env\Scripts\activate.bat

python main.py

deactivate
