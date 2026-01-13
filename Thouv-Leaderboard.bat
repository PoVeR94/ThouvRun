@echo off
REM ========================================
REM Lanceur - Serveur API Leaderboard
REM ========================================
cls
echo.
echo ========================================
echo   SERVEUR API LEADERBOARD THOUV'RUN
echo ========================================
echo.
echo [*] Demarrage du serveur sur http://localhost:5000
echo.
echo Pour acceder au leaderboard:
echo   http://localhost:5000/scores.html
echo.
echo Pour arreter le serveur:
echo   CTRL+C
echo.
echo ========================================
echo.

python api_server.py

if errorlevel 1 (
    echo.
    echo [!] ERREUR lors du lancement du serveur
    echo.
    echo Solutions:
    echo 1. Assure-toi que Flask et Flask-CORS sont installes:
    echo    pip install flask flask-cors
    echo.
    echo 2. Assure-toi qu'aucun autre programme n'utilise le port 5000
    echo.
    echo 3. Verifie que api_server.py existe dans le dossier courant
    echo.
    pause
    exit /b 1
)

pause
