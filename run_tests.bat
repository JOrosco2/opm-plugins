@echo off
setlocal enabledelayedexpansion

echo === Running Plugin Unit Tests ===

REM Step 1: Try to find Python manually
set PYTHON_EXE=

if exist "%LocalAppData%\Programs\Python\Python311\python.exe" (
    set PYTHON_EXE=%LocalAppData%\Programs\Python\Python311\python.exe
) else if exist "%LocalAppData%\Programs\Python\Python312\python.exe" (
    set PYTHON_EXE=%LocalAppData%\Programs\Python\Python312\python.exe
) else if exist "%LocalAppData%\Programs\Python\Python313\python.exe" (
    set PYTHON_EXE=%LocalAppData%\Programs\Python\Python313\python.exe
) else if exist "C:\Python311\python.exe" (
    set PYTHON_EXE=C:\Python311\python.exe
) else if exist "C:\Python312\python.exe" (
    set PYTHON_EXE=C:\Python312\python.exe
)

if not defined PYTHON_EXE (
    echo [!] Python could not be found.
    echo     Please install Python from https://python.org
    pause
    exit /b 1
)

echo [✓] Found Python: %PYTHON_EXE%

REM Step 2: Ensure pytest is installed
echo [*] Checking for pytest...
"%PYTHON_EXE%" -m pip install --quiet --disable-pip-version-check pytest

REM Step 3: Run tests
echo [*] Running tests...
"%PYTHON_EXE%" -m pytest tests -s

pause
