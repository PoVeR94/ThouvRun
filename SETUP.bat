@echo off
REM ========================================
REM SETUP Thouv'Run - Installation automatique
REM ========================================

echo.
echo ========================================
echo   SETUP - Thouv'Run Multi-Joueur
echo ========================================
echo.
echo Si tu vois ce message, le script fonctionne!
echo.
pause
echo.

echo [*] Verification de Python...
python --version
echo.
echo Resultat ci-dessus. Appuie sur une touche...
pause
echo.

echo [*] Verification de pip...
python -m pip --version
echo.
echo Resultat ci-dessus. Appuie sur une touche...
pause
echo.

echo [*] Installation des dependances...
echo     Cela peut prendre quelques minutes...
echo.
python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pygame windows-curses flask flask-cors requests
echo.
echo Resultat ci-dessus. Appuie sur une touche...
pause
echo.

echo ========================================
echo   INSTALLATION TERMINEE!
echo ========================================
echo.
echo Tu peux maintenant lancer:
echo   - Thouv-Run-Graphique.bat (jeu graphique)
echo   - Thouv-Run-Terminal.bat (jeu terminal)
echo.
pause
