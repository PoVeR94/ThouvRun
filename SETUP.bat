@echo off
REM ========================================
REM SETUP Thouv'Run - Installation automatique
REM ========================================
setlocal enabledelayedexpansion

cls
echo.
echo ========================================
echo   INSTALLATION DE THOUV'RUN
echo ========================================
echo.

REM Verifier Python
echo [*] Verification de Python...
python --version >nul 2>&1

if errorlevel 1 (
    echo.
    echo [!] ERREUR: Python n'est pas installe ou pas dans le PATH
    echo.
    echo Solutions:
    echo 1. Telecharge Python depuis: https://www.python.org/downloads/
    echo 2. Coche "Add Python to PATH" durant l'installation
    echo 3. Redémarre ton ordinateur
    echo 4. Relance ce script
    echo.
    pause
    exit /b 1
)

echo [OK] Python trouve!
python --version
echo.

REM Verifier pip
echo [*] Verification de pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [!] ERREUR: pip n'est pas disponible
    pause
    exit /b 1
)
echo [OK] pip disponible
echo.

REM Installer pygame
echo [*] Installation de pygame...
pip install pygame --quiet
if errorlevel 1 (
    echo [!] ERREUR lors de l'installation de pygame
    pause
    exit /b 1
)
echo [OK] pygame installe
echo.

REM Installer windows-curses
echo [*] Installation de windows-curses...
pip install windows-curses --quiet
if errorlevel 1 (
    echo [!] ERREUR lors de l'installation de windows-curses
    pause
    exit /b 1
)
echo [OK] windows-curses installe
echo.

REM Installer flask (pour leaderboard API)
echo [*] Installation de flask...
pip install flask flask-cors --quiet
if errorlevel 1 (
    echo [!] ERREUR lors de l'installation de flask
    pause
    exit /b 1
)
echo [OK] flask installe
echo.

REM Installer requests (pour synchronisation scores)
echo [*] Installation de requests...
pip install requests --quiet
if errorlevel 1 (
    echo [!] ERREUR lors de l'installation de requests
    pause
    exit /b 1
)
echo [OK] requests installe
echo.

REM Verifier que tout fonctionne
echo [*] Verification finale...
python -c "import pygame; import curses; import flask; import requests; print('[OK] Tous les modules charges!')" >nul 2>&1
if errorlevel 1 (
    echo [!] ERREUR: Les modules n'ont pas pu etre charges
    pause
    exit /b 1
)

cls
echo.
echo ========================================
echo   [OK] INSTALLATION REUSSIE!
echo ========================================
echo.
echo Tu peux maintenant jouer:
echo.
echo   -> Double-clique sur Thouv-Run-Graphique.bat
echo      (Version Pygame coloree et fluide)
echo.
echo   -> Double-clique sur Thouv-Run-Terminal.bat
echo      (Version texte retro)
echo.
echo BONUS - Leaderboard en temps reel:
echo.
echo   -> Lance le serveur API:
echo      python api_server.py
echo.
echo   -> Ouvre le leaderboard:
echo      http://localhost:5000/scores.html
echo.
echo   Pour plus de details: Lis LEADERBOARD.md
echo.
pause
