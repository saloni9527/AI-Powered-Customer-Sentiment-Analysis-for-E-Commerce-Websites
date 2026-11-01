@echo off
cd /d "%~dp0"
echo Using: "%~dp0.venv\Scripts\python.exe"
"%~dp0.venv\Scripts\python.exe" -m pip install -r "%~dp0requirements.txt"
echo.
"%~dp0.venv\Scripts\python.exe" -c "import bs4; print('bs4 OK')"
pause
