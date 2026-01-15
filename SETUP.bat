@echo off
REM ========================================
REM SETUP Thouv'Run - Installation automatique
REM ========================================

cls
echo.
echo ========================================
echo   SETUP - Thouv'Run Multi-Joueur
echo ========================================
echo.

REM Verifier Python
echo [*] Verification de Python...
python --version >nul 2>&1

if errorlevel 1 (
    echo.
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH
    echo.
    echo SOLUTIONS:
    echo 1. Telecharge Python 3.12: https://www.python.org/downloads/
    echo 2. IMPORTANT: Coche "Add Python to PATH" durant l'installation
    echo 3. Une fois termine, ferme ce script et relance-le
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
    echo [ERREUR] pip n'est pas disponible
    pause
    exit /b 1
)
echo [OK] pip disponible
echo.

REM ========================================
REM INSTALLATION DES DEPENDANCES
REM ========================================
echo [*] Installation des dependances...
echo     - pygame (graphique)
echo     - windows-curses (terminal)
echo     - flask (API serveur)
echo     - flask-cors (API)
echo     - requests (sync scores)
echo.

REM Installer les dépendances avec requirements-dev.txt
pip install -r requirements-dev.txt

if errorlevel 1 (
    echo.
    echo [ERREUR] Erreur lors de l'installation des dependances
    pause
    exit /b 1
)

echo.
echo ========================================
echo [OK] INSTALLATION REUSSIE!
echo ========================================
echo.
echo Tu peux maintenant:
echo   - Double-clic sur Thouv-Run-Graphique.bat (jeu pygame)
echo   - Double-clic sur Thouv-Run-Terminal.bat (jeu terminal)
echo   - Double-clic sur Thouv-Leaderboard.bat (voir les scores)
echo.
echo Ou lancer depuis PowerShell:
echo   python src/main_graphique.py
echo   python src/main_terminal.py
echo   python server/api_server.py
echo.
pause
