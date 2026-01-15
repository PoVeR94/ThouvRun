@echo off
REM ========================================
REM SETUP Thouv'Run - Installation automatique
REM ========================================
setlocal enabledelayedexpansion

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
    echo [*] Python non detecte, installation automatique...
    echo.
    
    REM Telecharger et installer Python (sans PowerShell pour eviter les problemes de policies)
    set "pythonUrl=https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe"
    set "pythonInstaller=%TEMP%\python-installer.exe"
    
    echo [*] Telechargement de Python (cela peut prendre 1-2 minutes)...
    
    REM Utiliser certutil (disponible sur tous les Windows) pour telecharger
    certutil -urlcache -split -f "!pythonUrl!" "!pythonInstaller!" >nul 2>&1
    
    if not exist "!pythonInstaller!" (
        echo [ERREUR] Impossible de telecharger Python
        echo Essaye une installation manuelle: https://www.python.org/downloads/
        pause
        exit /b 1
    )
    
    echo [*] Installation de Python...
    "!pythonInstaller!" /quiet InstallAllUsers=1 PrependPath=1
    
    del "!pythonInstaller!" /f /q 2>nul
    
    if errorlevel 1 (
        echo [ERREUR] Impossible d'installer Python
        pause
        exit /b 1
    )
    
    echo.
    echo [OK] Python installe!
    echo.
    echo Appuie sur une touche pour continuer...
    pause
    REM Relancer le script automatiquement
    call "%~f0"
    exit /b 0
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
