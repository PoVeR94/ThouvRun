@echo off
REM ========================================
REM Thouv'Run - Jeu Terminal (Curses)
REM DEPRECATED - Use: ..\Thouv-Run-Terminal.bat
REM ========================================

REM Redirection vers le fichier root
cd /d "%~dp0.."
call Thouv-Run-Terminal.bat


python src/main_terminal.py

if errorlevel 1 (
    echo.
    echo [ERREUR] Le jeu n'a pas pu demarrer
    echo.
    pause
)
