### @echo off

REM Activate virtual environment
call env/Scripts/activate

REM Set necessary environment variables
set PYTHONPATH=.

REM Run Pyinstaller
pyinstaller ^
--name="Youtube Downloader" ^
--clean ^
--onefile ^
./main.py