@echo off
setlocal
cd /d "%~dp0" || goto failed
set PYTHONUTF8=1
where git >nul 2>&1 || (echo Install Git for Windows first. & goto failed)
where gh >nul 2>&1 || (echo Install GitHub CLI first. & goto failed)
set "BOOT=py -3"
%BOOT% -c "import sys;sys.exit(sys.version_info < (3,11))" >nul 2>&1 && goto python_ok
set "BOOT=python"
%BOOT% -c "import sys;sys.exit(sys.version_info < (3,11))" >nul 2>&1 || (echo Python 3.11 or newer is required. & goto failed)
:python_ok
%BOOT% -m venv .venv || goto failed
set "PY=.venv\Scripts\python.exe"
"%PY%" -m pip --isolated --disable-pip-version-check install --no-index --only-binary=:all: --find-links wheels --require-hashes -r requirements.txt || goto failed
"%PY%" -m pip check || goto failed
"%PY%" -m unittest -v || goto failed
"%PY%" setup_project.py || goto failed
pause
exit /b 0
:failed
echo Setup stopped. See the message above.
pause
exit /b 1
