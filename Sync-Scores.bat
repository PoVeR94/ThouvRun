@echo off
chcp 65001 > nul
color 0B
echo.
echo ╔════════════════════════════════════════════╗
echo ║  THOUV'RUN - SYNCHRONISATION DES SCORES   ║
echo ╚════════════════════════════════════════════╝
echo.

REM Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé!
    echo Installez Python depuis https://www.python.org
    pause
    exit /b 1
)

REM Vérifier que requests est installé
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installation de requests...
    python -m pip install requests --quiet
)

echo 🚀 Lancement de la synchronisation...
echo.

python sync_scores_to_server.py

echo.
echo ✅ Synchronisation terminée!
echo.
echo 🌐 Vérifiez les scores sur:
echo    https://thouvrun.onrender.com/scores.html
echo.
pause
