@echo off
REM ========================================
REM SETUP Thouv'Run - Installation automatique
REM ========================================

echo.
echo ========================================
echo   SETUP - Thouv'Run Multi-Joueur
echo ========================================
echo.

REM ========================================
REM ETAPE 1: VERIFIER PYTHON
REM ========================================
echo [*] Verification de Python...
python --version >nul 2>&1
if errorlevel 1 goto INSTALL_PYTHON

echo [OK] Python trouve!
python --version
goto CHECK_PIP

:INSTALL_PYTHON
echo.
echo [!] Python n'est pas installe!
echo.
echo [*] Telechargement de Python 3.12...
echo     Cela peut prendre 1-2 minutes...
echo.
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe' -OutFile '%TEMP%\python-installer.exe'"

if not exist "%TEMP%\python-installer.exe" (
    echo.
    echo [ERREUR] Telechargement echoue!
    echo.
    echo Telecharge Python manuellement:
    echo https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe
    echo.
    echo IMPORTANT: Coche "Add Python to PATH" en bas!
    echo.
    pause
    exit /b 1
)

echo [OK] Python telecharge!
echo.
echo [*] Installation de Python...
echo.
echo ========================================
echo IMPORTANT: COCHE "Add Python to PATH"
echo en bas de la fenetre d'installation!
echo ========================================
echo.
pause

"%TEMP%\python-installer.exe"

del "%TEMP%\python-installer.exe" 2>nul

echo.
echo [OK] Python installe!
echo.
echo ========================================
echo FERME cette fenetre et RELANCE SETUP.bat
echo ========================================
echo.
pause
exit /b 0

:CHECK_PIP
echo.
echo [*] Verification de pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [!] pip non trouve, reinstallation...
    python -m ensurepip --upgrade
)
echo [OK] pip disponible!
echo.

REM ========================================
REM ETAPE 2: INSTALLER LES DEPENDANCES
REM ========================================
echo [*] Installation des dependances...
echo     - pygame
echo     - windows-curses  
echo     - flask, flask-cors
echo     - requests
echo.
echo     Cela peut prendre quelques minutes...
echo.

python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pygame windows-curses flask flask-cors requests

if errorlevel 1 (
    echo.
    echo [!] Erreur, essai avec mirror alternatif...
    python -m pip install --index-url https://pypi.tsinghua.edu.cn/simple --trusted-host pypi.tsinghua.edu.cn pygame windows-curses flask flask-cors requests
)

echo.
echo ========================================
echo [OK] INSTALLATION TERMINEE!
echo ========================================
echo.
echo Tu peux maintenant lancer:
echo   - Thouv-Run-Graphique.bat (jeu graphique)
echo   - Thouv-Run-Terminal.bat (jeu terminal)
echo.
pause
