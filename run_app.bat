@echo off
echo ==========================================
echo Biometric Attendance System Launcher
echo ==========================================

cd /d "%~dp0"

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

if not exist "venv\Lib\site-packages\installed_deps.flag" (
    echo Installing dependencies...
    pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo Error installing dependencies!
        echo Please ensure you have "Desktop development with C++" installed via Visual Studio Build Tools for dlib.
        pause
        exit /b
    )
    echoDependencies installed > venv\Lib\site-packages\installed_deps.flag
)

echo.
echo Starting Application...
python main.py

pause
