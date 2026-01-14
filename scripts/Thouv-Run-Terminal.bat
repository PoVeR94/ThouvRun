@echo off
REM ========================================
REM Thouv'Run - Jeu Terminal (Curses)
REM ========================================

setlocal enabledelayedexpansion

cd /d "%~dp0.."

REM Verifier que les dependances sont installees
python -c "import windows_curses, requests, flask" >nul 2>&1

if errorlevel 1 (
    echo.
    echo [!] Les dependances ne sont pas installees
    echo.
    echo Lancement du SETUP...
    echo.
    call scripts\SETUP.bat
    if errorlevel 1 (
        echo Installation echouee. Impossible de demarrer le jeu.
        pause
        exit /b 1
    )
)

REM Lancer le jeu terminal
echo.
echo ========================================
echo   Thouv'Run - Version Terminal
echo ========================================
echo.
echo Controles:
echo   Z ou UP     = Sauter
echo   ESC         = Pause / Retour
echo   P           = Pause Menu
echo.
echo Scores envoyes a: https://thouvrun-production.up.railway.app
echo.

python src/main_terminal.py

if errorlevel 1 (
    echo.
    echo [ERREUR] Le jeu n'a pas pu demarrer
    echo.
    pause
)
