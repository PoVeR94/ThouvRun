@echo off
REM ========================================
REM Thouv'Run - Leaderboard Web (API Serveur)
REM ========================================

setlocal enabledelayedexpansion

cd /d "%~dp0"

REM Verifier que les dependances sont installees
python -c "import flask, requests" >nul 2>&1

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
echo.
echo ========================================
echo   Thouv'Run - Leaderboard Web
echo ========================================
echo.
echo Le serveur demarre sur: http://localhost:5000
echo.
echo Ouverture du navigateur...
echo.

REM Ouvrir le navigateur automatiquement
timeout /t 2 /nobreak >nul
start http://localhost:5000

REM Lancer le serveur API
python api_server.py

if errorlevel 1 (
    echo.
    echo [ERREUR] Le serveur n'a pas pu demarrer
    echo.
    echo Assurez-vous que le port 5000 n'est pas utilise
    echo.
    pause
)
