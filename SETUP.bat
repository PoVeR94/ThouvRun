@echo off
REM ========================================
REM SETUP Thouv'Run - Installation automatique
REM Windows
REM ========================================

cls
echo.
echo ========================================
echo   SETUP - Thouv'Run Multi-Joueur
echo ========================================
echo.
echo [*] Systeme detecte: Windows
echo.

REM ========================================
REM INSTALLATION DE PYTHON
REM ========================================
echo [*] Verification de Python...
python --version >nul 2>&1

if errorlevel 1 (
    echo.
    echo [!] Python non installe, installation automatique...
    echo.
    
    REM Telecharger Python avec PowerShell
    echo [*] Telechargement de Python 3.12...
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe' -OutFile '%TEMP%\python-installer.exe'}"
    
    if not exist "%TEMP%\python-installer.exe" (
        echo.
        echo [ERREUR] Impossible de telecharger Python
        echo.
        echo Telecharge manuellement: https://www.python.org/downloads/
        echo IMPORTANT: Coche "Add Python to PATH" durant l'installation
        echo.
        pause
        exit /b 1
    )
    
    echo [*] Installation de Python 3.12 (avec PATH)...
    "%TEMP%\python-installer.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1
    
    if errorlevel 1 (
        echo.
        echo [!] Installation silencieuse echouee, lancement manuel...
        echo.
        echo IMPORTANT: Coche "Add Python to PATH" en bas de la fenetre!
        echo.
        "%TEMP%\python-installer.exe"
    )
    
    REM Nettoyer
    del "%TEMP%\python-installer.exe" 2>nul
    
    echo.
    echo [OK] Python installe!
    echo.
    echo [*] Relancement automatique du script...
    echo.
    
    REM Relancer le script automatiquement
    start "" "%~f0"
    exit /b 0
)

echo [OK] Python trouve!
python --version
echo.

REM ========================================
REM VERIFICATION DE PIP
REM ========================================
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

REM Mettre a jour pip d'abord
python -m pip install --upgrade pip >nul 2>&1

REM Installer les dependances (avec trusted-host pour eviter SSL)
python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements-dev.txt

if errorlevel 1 (
    echo.
    echo [!] Premiere tentative echouee, essai avec mirror alternatif...
    echo.
    
    REM Tentative 2: Mirror Tsinghua
    python -m pip install --index-url https://pypi.tsinghua.edu.cn/simple --trusted-host pypi.tsinghua.edu.cn -r requirements-dev.txt
    
    if errorlevel 1 (
        echo.
        echo [ERREUR] Impossible d'installer les dependances
        echo.
        echo Solutions:
        echo 1. Verifiez votre connexion internet
        echo 2. Desactivez temporairement l'antivirus
        echo 3. Verifiez l'heure du PC ^(clic-droit horloge^)
        echo.
        echo Installation manuelle dans PowerShell:
        echo   python -m pip install pygame windows-curses flask flask-cors requests
        echo.
        pause
        exit /b 1
    )
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
