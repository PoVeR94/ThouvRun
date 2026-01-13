@echo off
REM Lanceur Thouv'Run - Version Terminal
REM Lance le jeu en mode terminal

cd /d "%~dp0"
python main_terminal_launcher.py %*
if errorlevel 1 pause
