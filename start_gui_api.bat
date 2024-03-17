@echo off

if not exist env\Scripts\activate.bat (
    echo Creating virtual environment 'env'...
    python -m venv env
    call env\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
    deactivate
)

call env\Scripts\activate.bat

python api_version\mainapi.py

deactivate
PAUSE