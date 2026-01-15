@echo off
REM ========================================
REM Thouv'Run - Jeu Terminal (Curses)
REM ========================================

cd /d "%~dp0"

REM Lancer le jeu terminal
python src/main_terminal.py

if errorlevel 1 (
    echo.
    echo [ERREUR] Le jeu n'a pas pu demarrer
    echo.
    pause
)
