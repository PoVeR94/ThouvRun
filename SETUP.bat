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
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [!] pip non detecte, reinstallation automatique...
    echo.
    python -m ensurepip --upgrade
    
    if errorlevel 1 (
        echo [ERREUR] Impossible de reinstaller pip
        echo.
        echo Solutions:
        echo 1. Reinstalle Python 3.12: https://www.python.org/downloads/
        echo 2. Coche "Add Python to PATH" durant l'installation
        echo 3. Relance ce script
        echo.
        pause
        exit /b 1
    )
    
    echo [OK] pip reinstalle!
    echo.
)
echo [OK] pip disponible (via python -m pip)
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

REM Fixer certificats SSL + installer dependances
python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements-dev.txt

if errorlevel 1 (
    echo.
    echo [ERREUR] Impossible d'installer les dependances
    pause
    exit /b 1
)

echo [OK] Dependances installees!

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
