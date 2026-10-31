@echo off
cd /d "%~dp0"

:: Khoi dong che do cua so ngam khong hien thi Terminal (Zero Console Window)
if exist "%~dp0.venv\Scripts\pythonw.exe" (
    start "" "%~dp0.venv\Scripts\pythonw.exe" main.py
    exit /b 0
)

if exist "%~dp0.venv\Scripts\python.exe" (
    start "" "%~dp0.venv\Scripts\python.exe" main.py
    exit /b 0
)

where uv >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    start "" uv run pythonw main.py
    exit /b 0
)

if exist "%USERPROFILE%\.local\bin\uv.exe" (
    start "" "%USERPROFILE%\.local\bin\uv.exe" run pythonw main.py
    exit /b 0
)

start "" pythonw main.py 2>nul || start "" python main.py
exit /b 0
