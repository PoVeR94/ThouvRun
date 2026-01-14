@echo off
REM ========================================
REM Thouv'Run - Leaderboard en ligne
REM ========================================

setlocal enabledelayedexpansion

cd /d "%~dp0"

REM Verifier que les dependances sont installees
python -c "import flask, flask_cors" >nul 2>&1

if errorlevel 1 (
    echo.
    echo [!] Les dependances ne sont pas installees
    echo.
    echo Lancement du SETUP...
    echo.
    call SETUP.bat
    if errorlevel 1 (
        echo Installation echouee. Impossible de demarrer le serveur.
        pause
        exit /b 1
    )
)

REM Lancer le serveur API
python server/api_server.py

if errorlevel 1 (
    echo.
    echo [ERREUR] Le serveur n'a pas pu demarrer
    echo.
    pause
)
